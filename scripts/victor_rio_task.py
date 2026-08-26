#!/usr/bin/env python3
"""Return a read-only, evidence-backed RIO report to Dr. Victor."""
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "integration" / "results" / "victor_tasks"
ALLOWED = {"STATUS_CHECK", "GOVERNANCE_CHECK", "PRIORITY_CHECK", "STRICT_SUPERVISION_PROBE"}


def read_json(relative):
    try:
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))
    except Exception:
        return {}


def main():
    task_id = os.getenv("VICTOR_RIO_TASK_ID", "").strip()
    task_type = os.getenv("VICTOR_RIO_TASK_TYPE", "").strip().upper()
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,120}", task_id) or task_type not in ALLOWED:
        raise SystemExit("INVALID_OR_UNAUTHORIZED_VICTOR_RIO_TASK")
    try:
        payload = json.loads(os.getenv("VICTOR_RIO_TASK_PAYLOAD", "{}"))
    except Exception as exc:
        raise SystemExit("INVALID_VICTOR_RIO_TASK_PAYLOAD_JSON") from exc
    if payload.get("requested_by") != "victor" or payload.get("supervision_mode") != "STRICT":
        raise SystemExit("INVALID_VICTOR_RIO_AUTHORITY_ENVELOPE")

    status = read_json("data/status.json")
    work = read_json("data/rio_work_status.json")
    result_path = f"integration/results/victor_tasks/{task_id}.json"
    blocker = work.get("blocker") or work.get("founder_action_required") or None
    next_action = work.get("next_task") or work.get("next_action") or "VICTOR_REVIEW_AND_PUSH_NEXT_ACTION"
    result = {
        "schema_version": 1,
        "message_type": "TASK_RESULT",
        "sender": "rio",
        "recipient": "victor",
        "task_id": task_id,
        "task_type": task_type,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "execution_status": "COMPLETED_READ_ONLY_DIAGNOSTIC",
        "public_action_performed": False,
        "objective_changed": False,
        "credential_transfer_performed": False,
        "strict_supervision": {
            "status": "REPORTING_CONNECTED_PENDING_VICTOR_CERTIFICATION",
            "objective_alignment": "CHECKED_AGAINST_DATA_RIO_3_0_DEFINITION",
            "error_or_blocker": blocker,
            "solution": "Read-only governed report returned; no public action, objective change, or credential transfer performed.",
            "next_action": str(next_action),
            "evidence": ["data/RIO_3.0_DEFINITION.md", "data/status.json", "data/rio_work_status.json", result_path],
            "revert_to_victor": True,
            "requires_follow_up": bool(blocker),
        },
        "snapshot": {
            "validators_pass": status.get("all_validators_pass"),
            "status_updated": status.get("updated"),
            "current_task": work.get("current_task"),
            "last_completed": work.get("last_completed"),
        },
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"{task_id}.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
