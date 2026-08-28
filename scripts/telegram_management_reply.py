#!/usr/bin/env python3
"""Publish a verified Victor↔RIO result to the Telegram management group as RIO."""

import json
import os
import sys

from telegram_notify import send_telegram


def build_reply(result):
    strict = result.get("strict_supervision") or {}
    evidence = strict.get("evidence") or []
    evidence_text = ", ".join(str(item) for item in evidence[:3]) or "not provided"
    return "\n".join(
        [
            "RIO management-group revert",
            f"Status: {strict.get('status') or result.get('execution_status') or 'UNKNOWN'}",
            f"Objective alignment: {strict.get('objective_alignment') or 'UNKNOWN'}",
            f"Solution: {strict.get('solution') or 'NOT_PROVIDED'}",
            f"Next action: {strict.get('next_action') or 'NOT_PROVIDED'}",
            f"Evidence: {evidence_text}",
            f"Task ID: {result.get('task_id') or 'UNKNOWN'}",
        ]
    )


def main():
    task_id = (os.environ.get("VICTOR_RIO_TASK_ID") or "").strip()
    management_chat_id = (os.environ.get("TELEGRAM_MANAGEMENT_CHAT_ID") or "").strip()
    if not task_id or not management_chat_id:
        print("[management-reply] BLOCKED: task ID or management chat ID missing")
        return 2
    path = os.path.join("integration", "results", "victor_tasks", f"{task_id}.json")
    with open(path, encoding="utf-8") as handle:
        result = json.load(handle)
    if result.get("task_id") != task_id or result.get("sender") != "rio":
        print("[management-reply] BLOCKED: unverified RIO result envelope")
        return 3
    os.environ["TELEGRAM_CHAT_ID_RIO"] = management_chat_id
    ok, detail = send_telegram(build_reply(result))
    print(f"[management-reply] {detail}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
