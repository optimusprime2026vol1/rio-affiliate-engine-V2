#!/usr/bin/env python3
"""Run one safe objective-driven RIO business cycle from persistent work memory."""
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from telegram_chat import call_llm
from rio_autonomous_executor import execute as execute_plan
from rio_work_dashboard import record

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "data" / "rio_work_status.json"
SNAPSHOT = ROOT / "data" / "dashboard_snapshot.json"
STATUS = ROOT / "data" / "status.json"
CONTROL = ROOT / "data" / "control.json"
AUDIT = ROOT / "data" / "autonomy_audit.jsonl"
BOT = (os.environ.get("TELEGRAM_BOT_TOKEN_RIO") or "").strip()
CHAT = (os.environ.get("TELEGRAM_CHAT_ID_RIO") or "").strip()


def jload(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def tail_audit(limit=6):
    try:
        lines = AUDIT.read_text(encoding="utf-8").splitlines()[-limit:]
        return [json.loads(x) for x in lines if x.strip()]
    except Exception:
        return []


def notify(text):
    if not BOT or not CHAT:
        return False
    data = urllib.parse.urlencode({"chat_id": CHAT, "text": text, "disable_web_page_preview": True}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{BOT}/sendMessage", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return bool(json.load(r).get("ok"))
    except Exception as e:
        print("[autonomous_cycle] Telegram notify failed:", e)
        return False


def completed_task_keys(memory, limit=12):
    keys = []
    for item in reversed(memory.get("history") or []):
        if item.get("status") != "COMPLETED":
            continue
        task = " ".join(str(item.get("task") or "").lower().split())
        if task and task not in keys:
            keys.append(task)
        if len(keys) >= limit:
            break
    return keys


def main():
    control = jload(CONTROL, {"kill_switch": False})
    memory = jload(WORK, {})
    snapshot = jload(SNAPSHOT, {})
    health = jload(STATUS, {})

    if control.get("kill_switch"):
        print("[autonomous_cycle] skipped: kill switch ON")
        return 0
    if health.get("all_validators_pass") is not True:
        print("[autonomous_cycle] skipped: heartbeat validators are not healthy")
        return 0
    if memory.get("status") == "WORKING":
        print("[autonomous_cycle] skipped: previous work still marked WORKING")
        return 0
    if memory.get("founder_action_needed") or memory.get("status") in {"BLOCKED", "VICKY_ACTION_REQUIRED"}:
        print("[autonomous_cycle] paused on Founder blocker")
        return 0

    recent_completed = completed_task_keys(memory)
    memory_context = {
        "status": memory.get("status", "IDLE"),
        "last_completed": memory.get("last_completed"),
        "last_result": memory.get("last_result"),
        "next_task": memory.get("next_task"),
        "changed_files": memory.get("changed_files") or [],
        "recent_completed_task_keys": recent_completed,
        "recent_history": (memory.get("history") or [])[-12:],
        "recent_audit": tail_audit(),
        "business_snapshot": {
            "ready_offers": snapshot.get("ready_offers", 0),
            "blocked_offers": snapshot.get("blocked_offers", 0),
            "content_items": snapshot.get("content_items", 0),
            "revenue_inr": snapshot.get("revenue_inr", 0),
            "net_profit_inr": snapshot.get("net_profit_inr", 0),
            "instagram_posted": snapshot.get("instagram_posted", 0),
        },
    }

    instruction = (
        "AUTONOMOUS PHASE-2 CYCLE. Continue RIO's locked business objective from persistent memory below. "
        "Choose EXACTLY ONE highest-impact safe repository task. NEVER repeat a recently COMPLETED task or recreate/overwrite the same deliverable merely because a future dependency is pending. "
        "Treat a next_task containing dependencies such as 'after this posts', 'monitor engagement', 'when data arrives', 'if CTR', 'wait', or any external event/metric not yet evidenced in memory as a WAIT STATE, not as permission to repeat the preceding task. "
        "When the preferred next_task is waiting on external evidence, explicitly pivot to a DIFFERENT independent safe task from another locked execution pillar that advances revenue/readiness. "
        "Before executing, compare your proposed task with recent_completed_task_keys and changed_files; if substantially equivalent, choose another task. "
        "Do not restart from zero. Do not create accounts, handle credentials, make payments/legal commitments, bypass verification, invent product facts, weaken validators, or claim external metrics without evidence. "
        "If no independent safe repository task exists, return intent=respond with prefix WAITING_EXTERNAL: and state exactly what evidence/event is awaited; this is NOT Founder action unless the Founder must actually do something. "
        "Your founder_message must include what task you chose, why, what changed, and a concrete NEXT_TASK:. "
        "Persistent memory:\n" + json.dumps(memory_context, ensure_ascii=False)
    )

    record("WORKING", current_task=memory.get("next_task") or "Selecting highest-impact safe Phase-2 task.", engine="selecting", validators="PRECHECK_PASS", founder_action_needed=False)
    plan, engine = call_llm([], instruction)
    summary = (plan.get("founder_message") or plan.get("summary") or "").strip()

    if plan.get("intent") != "execute":
        if summary.upper().startswith("WAITING_EXTERNAL:"):
            record("WAITING", current_task=memory.get("next_task") or "Waiting for external evidence", engine=engine, validators="NOT_RUN", result=summary, next_task=memory.get("next_task"), blocker=None, founder_action_needed=False)
            print("[autonomous_cycle] waiting on external evidence:", summary)
            return 0
        blocker = summary or "AI did not provide an executable safe task."
        record("VICKY_ACTION_REQUIRED", current_task=memory.get("next_task") or "Autonomous continuation", engine=engine, validators="NOT_RUN", result=blocker, blocker=blocker, founder_action_needed=True)
        notify("⚠️ RIO FOUNDER ACTION REQUIRED\n" + blocker[:3000])
        return 0

    chosen = (plan.get("summary") or memory.get("next_task") or "Autonomous Phase-2 task").strip()
    chosen_key = " ".join(chosen.lower().split())
    if chosen_key in recent_completed:
        record("WAITING", current_task=chosen, engine=engine, validators="NOT_RUN", result="ANTI_REPEAT: AI selected an already completed task; execution suppressed. Next cycle must choose a different independent task.", next_task="Choose a different independent safe task; do not repeat recent completed work.", blocker=None, founder_action_needed=False)
        print("[autonomous_cycle] anti-repeat suppressed duplicate task")
        return 0

    record("WORKING", current_task=chosen, engine=engine, validators="RUNNING", founder_action_needed=False)
    result = execute_plan(plan, request_summary="AUTONOMOUS PHASE-2: " + chosen, engine=engine)
    changed = result.get("changed_paths") or []

    if result.get("ok"):
        next_task = None
        marker = "next_task:"
        low = summary.lower()
        if marker in low:
            idx = low.rfind(marker)
            next_task = summary[idx + len(marker):].strip().splitlines()[0][:500] or None
        if not next_task:
            next_task = "Choose the next highest-impact safe task using objective, completed history, current business metrics, and anti-repeat rules."
        record("COMPLETED", current_task=chosen, engine=engine, changed_files=changed, validators="PASS", result=summary or "Autonomous task completed and validated.", next_task=next_task, blocker=None, founder_action_needed=False)
        print(json.dumps({"ok": True, "engine": engine, "task": chosen, "changed": changed, "next_task": next_task}, ensure_ascii=False))
        return 0

    status = result.get("status", "FAILED")
    error = result.get("error", "unknown")
    founder_needed = status == "VICKY_ACTION_REQUIRED"
    record(status, current_task=chosen, engine=engine, changed_files=[], validators="FAIL", result=summary or "Autonomous task failed and was not accepted.", next_task=memory.get("next_task"), blocker=error, founder_action_needed=founder_needed)
    if founder_needed:
        notify(f"⚠️ RIO FOUNDER ACTION REQUIRED\nTask: {chosen}\nBlocker: {error}"[:3500])
    print(json.dumps({"ok": False, "status": status, "engine": engine, "task": chosen, "error": error}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
