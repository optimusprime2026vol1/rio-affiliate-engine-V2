#!/usr/bin/env python3
"""Guarded executor for Founder instructions planned by DeepSeek.

The model may propose file operations; this module enforces path/operation policy,
runs fixed validators, rolls back failed runs, and writes an audit trail.
"""
import json
import os
import py_compile
import subprocess
from datetime import datetime, timezone, timedelta

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IST = timezone(timedelta(hours=5, minutes=30))
AUDIT = os.path.join(ROOT, "data", "autonomy_audit.jsonl")

PROTECTED = {
    ".gitignore",
    "data/RIO_3.0_DEFINITION.md",
    "data/AUTONOMY_POLICY.md",
    "data/TELEGRAM_CHAT_LOCKED.md",
    "scripts/rio_autonomous_executor.py",
    "scripts/telegram_chat.py",
}
ALLOWED_PREFIXES = ("data/", "site/", "scripts/")
ALLOWED_OPS = {"write_text", "write_json", "append_text"}
VALIDATORS = [
    "scripts/validate_offer_integrity.py",
    "scripts/validate_product_candidates.py",
    "scripts/validate_dashboard.py",
]


def _rel(path):
    path = (path or "").replace("\\", "/").lstrip("/")
    norm = os.path.normpath(path).replace("\\", "/")
    if norm.startswith("../") or norm == ".." or os.path.isabs(path):
        raise ValueError("path escapes repository")
    return norm


def _allowed(path):
    p = _rel(path)
    if p in PROTECTED or p.startswith(".github/workflows/"):
        return False
    return p.startswith(ALLOWED_PREFIXES)


def _audit(record):
    os.makedirs(os.path.dirname(AUDIT), exist_ok=True)
    with open(AUDIT, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _run(cmd):
    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=120)
    out = ((p.stdout or "") + (p.stderr or "")).strip()
    return p.returncode, out[-3000:]


def validate():
    results = []
    scripts_dir = os.path.join(ROOT, "scripts")
    try:
        for name in os.listdir(scripts_dir):
            if name.endswith(".py"):
                py_compile.compile(os.path.join(scripts_dir, name), doraise=True)
        results.append({"test": "python_compile", "ok": True, "output": "PASS"})
    except Exception as e:
        results.append({"test": "python_compile", "ok": False, "output": str(e)})
        return False, results
    for script in VALIDATORS:
        code, out = _run(["python", script])
        results.append({"test": script, "ok": code == 0, "output": out})
        if code != 0:
            return False, results
    return True, results


def execute(plan, request_summary="", engine="deepseek"):
    ts = datetime.now(IST).isoformat(timespec="seconds")
    risk = str(plan.get("risk") or "high").lower()
    ops = plan.get("operations") or []
    record = {"timestamp": ts, "request": request_summary[:500], "engine": engine,
              "risk": risk, "operations": [], "result": None, "changed_paths": [],
              "validators": []}

    if plan.get("intent") != "execute":
        record["result"] = "NO_EXECUTION"
        _audit(record)
        return {"ok": True, "status": "NO_EXECUTION", "changed_paths": [], "validators": []}
    if risk == "high":
        record["result"] = "BLOCKED_HIGH_RISK"
        _audit(record)
        return {"ok": False, "status": "VICKY_ACTION_REQUIRED", "error": "high-risk change blocked"}
    if not isinstance(ops, list) or not ops:
        record["result"] = "BLOCKED_EMPTY_PLAN"
        _audit(record)
        return {"ok": False, "status": "FAILED", "error": "empty execution plan"}
    if len(ops) > 8:
        record["result"] = "BLOCKED_TOO_MANY_OPERATIONS"
        _audit(record)
        return {"ok": False, "status": "VICKY_ACTION_REQUIRED", "error": "operation limit exceeded"}

    backups = {}
    created = set()
    try:
        for op in ops:
            kind = op.get("op")
            path = _rel(op.get("path"))
            if kind not in ALLOWED_OPS:
                raise ValueError(f"operation not allowed: {kind}")
            if not _allowed(path):
                raise PermissionError(f"protected/disallowed path: {path}")
            full = os.path.join(ROOT, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            if path not in backups:
                if os.path.exists(full):
                    with open(full, "rb") as f:
                        backups[path] = f.read()
                else:
                    backups[path] = None
                    created.add(path)
            if kind == "write_json":
                value = op.get("value")
                with open(full, "w", encoding="utf-8") as f:
                    json.dump(value, f, indent=2, ensure_ascii=False)
                    f.write("\n")
            else:
                content = str(op.get("content") or "")
                mode = "a" if kind == "append_text" else "w"
                with open(full, mode, encoding="utf-8") as f:
                    f.write(content)
            record["operations"].append({"op": kind, "path": path})
            record["changed_paths"].append(path)

        ok, checks = validate()
        record["validators"] = checks
        if not ok:
            raise RuntimeError("validation failed")
        record["result"] = "COMPLETED"
        _audit(record)
        return {"ok": True, "status": "COMPLETED", "changed_paths": record["changed_paths"], "validators": checks}
    except Exception as e:
        for path, old in backups.items():
            full = os.path.join(ROOT, path)
            try:
                if old is None:
                    if os.path.exists(full):
                        os.remove(full)
                else:
                    with open(full, "wb") as f:
                        f.write(old)
            except Exception:
                pass
        record["result"] = "FAILED_ROLLED_BACK"
        record["error"] = str(e)[:1000]
        _audit(record)
        return {"ok": False, "status": "FAILED_ROLLED_BACK", "error": str(e), "validators": record["validators"]}
