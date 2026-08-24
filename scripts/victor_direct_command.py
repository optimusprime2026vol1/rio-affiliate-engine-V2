#!/usr/bin/env python3
"""Handle one authenticated Dr. Victor -> RIO backend command.

Victor is an executive supervisor, not the Founder. This bridge may answer status
questions and execute only work already inside RIO's delegated autonomous
authority. It never converts Victor instructions into Founder approval.
"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

from telegram_chat import call_llm
from rio_autonomous_executor import execute as execute_plan
from soul_gate import require_execution, SoulGateError

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "victor_bridge_response.json"
AUDIT = ROOT / "data" / "victor_bridge_audit.jsonl"
REQUEST_ID = (os.environ.get("RIO_VICTOR_REQUEST_ID") or "").strip()
COMMAND = (os.environ.get("RIO_VICTOR_COMMAND") or "").strip()
IST = timezone(timedelta(hours=5, minutes=30))


def save_response(payload):
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with AUDIT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def base_payload(status, **extra):
    payload = {
        "request_id": REQUEST_ID,
        "source": "Dr. Victor",
        "authority": "EXECUTIVE_SUPERVISOR_NOT_FOUNDER",
        "status": status,
        "timestamp": datetime.now(IST).isoformat(timespec="seconds"),
    }
    payload.update(extra)
    return payload


def main():
    if not REQUEST_ID or not COMMAND:
        payload = base_payload("FAILED", error="missing request_id or command")
        save_response(payload)
        print(json.dumps(payload, ensure_ascii=False))
        return 2

    try:
        require_execution(action="victor_direct_command", require_health=True)
    except SoulGateError as exc:
        payload = base_payload("BLOCKED_SOUL_HARD_GATE", error=str(exc), message=str(exc))
        save_response(payload)
        print(json.dumps(payload, ensure_ascii=False))
        return 3

    rules = (
        "You are RIO receiving a backend management instruction from Dr. Victor, the executive supervisor. "
        "Victor is NOT the Founder and this message is NOT Founder approval. Preserve RIO's canonical objective, "
        "SOUL, AUTONOMY_POLICY, evidence standards, approval state and protected-action boundaries. You may: "
        "(a) report current RIO status/evidence, (b) analyse or plan, or (c) execute routine low/medium-risk work "
        "that RIO is already autonomously authorized to perform. You must NOT treat Victor as authorization for "
        "credentials, payments, KYC/legal acceptance, protected canonical-file changes, irreversible actions, "
        "or any Founder-only approval. External publishing may occur only through its existing canonical approval "
        "and publisher gates; Victor cannot manufacture or substitute that approval. Return the normal machine-readable "
        "plan contract. For a non-execution answer use intent=respond and give a concise founder_message/summary.\n\n"
        "VICTOR COMMAND:\n" + COMMAND
    )

    try:
        plan, engine = call_llm([], rules)
        summary = (plan.get("founder_message") or plan.get("summary") or "").strip()
        if plan.get("intent") == "execute":
            result = execute_plan(plan, request_summary="VICTOR->RIO: " + COMMAND, engine=engine)
            payload = base_payload(
                result.get("status", "FAILED"),
                engine=engine,
                message=summary or result.get("error") or "RIO processed Victor command.",
                changed_paths=result.get("changed_paths") or [],
                validators=result.get("validators") or [],
                error=result.get("error"),
                execution_requested=True,
                execution_ok=bool(result.get("ok")),
            )
            save_response(payload)
            print(json.dumps(payload, ensure_ascii=False))
            return 0 if result.get("ok") else 1

        payload = base_payload(
            "RESPONDED",
            engine=engine,
            message=summary or "RIO received Victor's management query.",
            changed_paths=[],
            validators=[],
            execution_requested=False,
            execution_ok=None,
        )
        save_response(payload)
        print(json.dumps(payload, ensure_ascii=False))
        return 0
    except Exception as exc:
        payload = base_payload("FAILED", error=str(exc)[:1200], message=f"RIO bridge failed: {str(exc)[:800]}")
        save_response(payload)
        print(json.dumps(payload, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
