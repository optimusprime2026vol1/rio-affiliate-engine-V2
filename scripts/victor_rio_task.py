#!/usr/bin/env python3
"""Return an evidence-backed RIO result to Dr. Victor.

Normal Victor probes remain read-only. A Victor Goal Contract may run one existing
RIO governed autonomous business cycle before this reporter is called; this file
only reports the resulting evidence and never bypasses RIO's own gates.
"""
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "integration" / "results" / "victor_tasks"
ALLOWED = {"STATUS_CHECK", "GOVERNANCE_CHECK", "PRIORITY_CHECK", "STRICT_SUPERVISION_PROBE", "GOAL_EXECUTE"}


def read_json(relative):
    try:
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))
    except Exception:
        return {}


def is_goal_contract(payload):
    text = str(payload.get("founder_message") or "")
    return "VICTOR GOAL CONTRACT" in text.upper() or payload.get("execution_mode") == "GOAL_EXECUTE"


def extract_goal_id(payload):
    text = str(payload.get("founder_message") or "")
    match = re.search(r"Goal ID:\s*([A-Za-z0-9._-]+)", text, re.I)
    return match.group(1) if match else payload.get("goal_id")


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
    snapshot = read_json("data/dashboard_snapshot.json")
    production = read_json("data/production_control.json")
    result_path = f"integration/results/victor_tasks/{task_id}.json"
    blocker = work.get("blocker") or work.get("founder_action_required") or None
    next_action = work.get("next_task") or work.get("next_action") or "VICTOR_REVIEW_AND_PUSH_NEXT_ACTION"
    goal_mode = is_goal_contract(payload)
    work_state = str(work.get("status") or "UNKNOWN").upper()
    founder_action = bool(work.get("founder_action_needed")) or work_state == "VICKY_ACTION_REQUIRED"
    changed = [str(x) for x in (work.get("changed_files") or []) if x]

    evidence = [
        "data/RIO_3.0_DEFINITION.md",
        "data/COMMERCIAL_VALIDATION_POLICY.json",
        "data/production_control.json",
        "data/status.json",
        "data/rio_work_status.json",
        "data/dashboard_snapshot.json",
        *changed,
        result_path,
    ]
    evidence = list(dict.fromkeys(evidence))

    if goal_mode:
        strict_status = "GOAL_PROGRESS_VERIFIED" if status.get("all_validators_pass") is True and not blocker else "GOAL_PROGRESS_BLOCKED"
        solution = "Existing governed RIO autonomous business cycle executed through RIO Soul, policy, validator and rollback controls; this report returns the resulting evidence to Victor."
        outcome_progress = {
            "rio_work_state": work_state,
            "last_completed": work.get("last_completed"),
            "ready_offers": snapshot.get("ready_offers"),
            "revenue_inr": snapshot.get("revenue_inr"),
            "production_state": production.get("production_state"),
        }
        requires_follow_up = not founder_action
        execution_status = "GOVERNED_GOAL_CYCLE_EXECUTED"
    else:
        strict_status = "REPORTING_CONNECTED_PENDING_VICTOR_CERTIFICATION"
        solution = "Read-only governed report returned; no public action, objective change, or credential transfer performed."
        outcome_progress = None
        requires_follow_up = bool(blocker)
        execution_status = "COMPLETED_READ_ONLY_DIAGNOSTIC"

    result = {
        "schema_version": 2,
        "message_type": "TASK_RESULT",
        "sender": "rio",
        "recipient": "victor",
        "task_id": task_id,
        "task_type": "GOAL_EXECUTE" if goal_mode else task_type,
        "goal_id": extract_goal_id(payload) if goal_mode else None,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "execution_status": execution_status,
        "governed_business_cycle_performed": goal_mode,
        "public_action_performed": False,
        "objective_changed": False,
        "credential_transfer_performed": False,
        "strict_supervision": {
            "status": strict_status,
            "goal_id": extract_goal_id(payload) if goal_mode else None,
            "objective_alignment": "CHECKED_AGAINST_DATA_RIO_3_0_DEFINITION",
            "outcome_progress": outcome_progress,
            "error_or_blocker": blocker,
            "solution": solution,
            "next_action": str(next_action),
            "evidence": evidence,
            "revert_to_victor": True,
            "requires_follow_up": requires_follow_up,
        },
        "snapshot": {
            "validators_pass": status.get("all_validators_pass"),
            "status_updated": status.get("updated"),
            "current_task": work.get("current_task"),
            "last_completed": work.get("last_completed"),
            "production_state": production.get("production_state"),
            "changed_files": changed,
        },
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"{task_id}.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
