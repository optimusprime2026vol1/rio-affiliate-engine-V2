#!/usr/bin/env python3
"""Stage only executor-authorized autonomous artifacts and canonical cycle evidence."""

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "autonomy_audit.jsonl"
ALLOWED_PREFIXES = ("data/", "site/", "scripts/")
PROTECTED = {
    ".gitignore",
    "data/RIO_3.0_DEFINITION.md",
    "data/AUTONOMY_POLICY.md",
    "data/TELEGRAM_CHAT_LOCKED.md",
    "data/SOUL.md",
    "data/soul_runtime_status.json",
    "scripts/soul_runtime.py",
    "scripts/heartbeat.py",
    "scripts/rio_autonomous_executor.py",
    "scripts/telegram_chat.py",
}
ALWAYS = {
    "data/rio_work_status.json",
    "data/autonomy_audit.jsonl",
    "data/control.json",
    "data/status.json",
    "data/dashboard_snapshot.json",
    "data/heartbeat_runner_status.json",
    "data/heartbeat_alert_state.json",
    "data/ceo_action_queue.csv",
    "site/dashboard/index.html",
}


def safe_path(value: str) -> str:
    path = str(value or "").replace("\\", "/").lstrip("/")
    if not path or path.startswith("../") or "/../" in f"/{path}/":
        raise ValueError(f"Unsafe autonomous path: {path}")
    if path in PROTECTED or path.startswith(".github/"):
        raise ValueError(f"Protected autonomous path: {path}")
    if not path.startswith(ALLOWED_PREFIXES):
        raise ValueError(f"Out-of-scope autonomous path: {path}")
    return path


def main() -> int:
    paths = set(ALWAYS)
    if AUDIT.exists():
        lines = [line for line in AUDIT.read_text(encoding="utf-8").splitlines() if line.strip()]
        if lines:
            record = json.loads(lines[-1])
            for value in record.get("changed_paths") or []:
                paths.add(safe_path(value))

    existing = [path for path in sorted(paths) if (ROOT / path).exists()]
    if existing:
        subprocess.run(["git", "add", "--", *existing], cwd=ROOT, check=True)
    print(json.dumps({"status": "SAFE_STAGE_OK", "paths": existing}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
