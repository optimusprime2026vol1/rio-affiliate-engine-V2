#!/usr/bin/env python3
"""SOUL runtime integrity layer — compatibility/observe mode.

This stage never stops RIO. It verifies that the portable SOUL can bind safely to
RIO's existing objective, memory, lead-AI configuration, heartbeat and validators.
Hard fail-closed enforcement is intentionally deferred to a later explicit stage.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOUL = ROOT / "data" / "SOUL.md"
OBJECTIVE = ROOT / "data" / "RIO_3.0_DEFINITION.md"
MEMORY = ROOT / "data" / "rio_work_status.json"
STATUS = ROOT / "data" / "status.json"
OUT = ROOT / "data" / "soul_runtime_status.json"

REQUIRED_MARKERS = (
    "# SOUL — Portable Autonomous Runtime Contract",
    "## Precedence",
    "## Seven Laws",
    "## Runtime Contract",
    "## AI Binding",
    "## Liveness Semantics",
)


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def load_json(path):
    try:
        return json.loads(read(path))
    except Exception:
        return {}


def inspect_runtime():
    soul = read(SOUL)
    objective = read(OBJECTIVE)
    memory = load_json(MEMORY)
    status = load_json(STATUS)
    checks = {
        "soul_present": bool(soul.strip()),
        "soul_contract_markers": bool(soul.strip()) and all(m in soul for m in REQUIRED_MARKERS),
        "objective_present": bool(objective.strip()),
        "memory_present": MEMORY.exists() and isinstance(memory, dict),
        "heartbeat_status_present": STATUS.exists() and isinstance(status, dict),
        "lead_ai_declared": bool(status.get("runtime_primary_ai")),
        "validators_declared": "all_validators_pass" in status,
    }
    valid = all(checks.values())
    result = {
        "mode": "compatibility_observe",
        "hard_fail_closed": False,
        "project_binding": "RIO",
        "valid": valid,
        "checks": checks,
        "soul_sha256": hashlib.sha256(soul.encode("utf-8")).hexdigest() if soul else None,
        "objective_path": "data/RIO_3.0_DEFINITION.md",
        "memory_path": "data/rio_work_status.json",
        "lead_ai": status.get("runtime_primary_ai"),
        "fallbacks": status.get("runtime_fallbacks") or [],
        "validators_currently_healthy": status.get("all_validators_pass"),
        "execution_effect": "NONE — observe-only; existing RIO gates remain authoritative",
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(inspect_runtime())
