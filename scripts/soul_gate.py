#!/usr/bin/env python3
"""RIO SOUL fail-closed governance gate.

Diagnostics may run while this gate is invalid, but consequential autonomous or
external business execution must not proceed. This module is deterministic and
is intended to be reused by workflows and executors rather than reimplementing
SOUL checks in each execution path.
"""
import argparse
import hashlib
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOUL = ROOT / "data" / "SOUL.md"
OBJECTIVE = ROOT / "data" / "RIO_3.0_DEFINITION.md"
POLICY = ROOT / "data" / "AUTONOMY_POLICY.md"
MEMORY = ROOT / "data" / "rio_work_status.json"
STATUS = ROOT / "data" / "status.json"
CONTROL = ROOT / "data" / "control.json"
OUT = ROOT / "data" / "soul_runtime_status.json"
IST = timezone(timedelta(hours=5, minutes=30))

SOUL_MARKERS = (
    "# SOUL — Portable Autonomous Runtime Contract",
    "## Precedence",
    "## Seven Laws",
    "## Runtime Contract",
    "## AI Binding",
    "## Liveness Semantics",
)
OBJECTIVE_MARKERS = (
    "# RIO 3.0 — Core Definition",
    "## 2. OBJECTIVE — FOUNDER LOCKED",
    "### Mandatory Phase-2 autonomous execution pillars — FOUNDER LOCKED",
)
POLICY_MARKERS = (
    "# RIO Autonomous Execution Policy",
    "## Authority model",
    "## Protected files / actions",
    "## Founder instruction persistence — mandatory",
)


class SoulGateError(RuntimeError):
    pass


def _read(path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _json(path, default):
    try:
        return json.loads(_read(path))
    except Exception:
        return default


def evaluate(action="consequential_execution", require_health=True, require_kill_clear=True, write_status=True):
    soul = _read(SOUL)
    objective = _read(OBJECTIVE)
    policy = _read(POLICY)
    memory = _json(MEMORY, None)
    status = _json(STATUS, None)
    control = _json(CONTROL, {})

    checks = {
        "soul_present": bool(soul.strip()),
        "soul_contract_markers": bool(soul.strip()) and all(m in soul for m in SOUL_MARKERS),
        "objective_present": bool(objective.strip()),
        "objective_lock_markers": bool(objective.strip()) and all(m in objective for m in OBJECTIVE_MARKERS),
        "authority_policy_present": bool(policy.strip()),
        "authority_policy_markers": bool(policy.strip()) and all(m in policy for m in POLICY_MARKERS),
        "memory_present": isinstance(memory, dict),
        "heartbeat_status_present": isinstance(status, dict),
        "lead_ai_declared": isinstance(status, dict) and bool(status.get("runtime_primary_ai")),
        "validators_declared": isinstance(status, dict) and "all_validators_pass" in status,
        "validators_healthy": (isinstance(status, dict) and status.get("all_validators_pass") is True) if require_health else True,
        "kill_switch_clear": (control.get("kill_switch") is not True) if require_kill_clear else True,
    }
    valid = all(checks.values())
    failed = [name for name, ok in checks.items() if ok is not True]
    result = {
        "mode": "hard_fail_closed",
        "hard_fail_closed": True,
        "project_binding": "RIO",
        "action": action,
        "valid": valid,
        "checks": checks,
        "failed_checks": failed,
        "soul_sha256": hashlib.sha256(soul.encode("utf-8")).hexdigest() if soul else None,
        "objective_sha256": hashlib.sha256(objective.encode("utf-8")).hexdigest() if objective else None,
        "authority_policy_sha256": hashlib.sha256(policy.encode("utf-8")).hexdigest() if policy else None,
        "objective_path": "data/RIO_3.0_DEFINITION.md",
        "authority_policy_path": "data/AUTONOMY_POLICY.md",
        "memory_path": "data/rio_work_status.json",
        "lead_ai": status.get("runtime_primary_ai") if isinstance(status, dict) else None,
        "fallbacks": status.get("runtime_fallbacks") or [] if isinstance(status, dict) else [],
        "validators_currently_healthy": status.get("all_validators_pass") if isinstance(status, dict) else None,
        "execution_effect": "ALLOWED" if valid else "CONSEQUENTIAL_EXECUTION_BLOCKED",
        "diagnostics_allowed": True,
        "checked_at": datetime.now(IST).isoformat(timespec="seconds"),
    }

    if write_status:
        OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if isinstance(status, dict):
            status["soul_runtime"] = {
                "mode": result["mode"],
                "valid": result["valid"],
                "hard_fail_closed": True,
                "soul_sha256": result["soul_sha256"],
                "objective_sha256": result["objective_sha256"],
                "authority_policy_sha256": result["authority_policy_sha256"],
                "failed_checks": failed,
                "execution_effect": result["execution_effect"],
                "checked_at": result["checked_at"],
            }
            STATUS.write_text(json.dumps(status, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


def require_execution(action="consequential_execution", require_health=True):
    result = evaluate(action=action, require_health=require_health, require_kill_clear=True, write_status=True)
    if not result["valid"]:
        failed = ", ".join(result["failed_checks"]) or "unknown governance failure"
        raise SoulGateError(
            f"SOUL_HARD_GATE blocked {action}. Failed checks: {failed}. "
            "Diagnostics/reporting remain available; consequential execution is fail-closed."
        )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", default="workflow_preflight")
    parser.add_argument("--no-health", action="store_true", help="diagnostic integrity check without requiring current validators healthy")
    args = parser.parse_args()
    result = evaluate(action=args.action, require_health=not args.no_health, require_kill_clear=True, write_status=True)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["valid"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
