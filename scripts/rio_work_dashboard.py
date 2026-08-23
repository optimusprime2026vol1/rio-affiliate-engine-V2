#!/usr/bin/env python3
"""RIO operational work-status tracker + dashboard renderer."""
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "rio_work_status.json"
SITE_DASH = ROOT / "site" / "rio-dashboard" / "index.html"
PUBLIC_DASH = ROOT / "rio-dashboard" / "index.html"
IST = timezone(timedelta(hours=5, minutes=30))


def now():
    return datetime.now(IST).isoformat(timespec="seconds")


def load():
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        return {
            "status": "IDLE",
            "current_task": "Waiting for next autonomous task.",
            "started_at": None,
            "updated_at": now(),
            "ai_engine": "unknown",
            "last_completed": None,
            "last_result": None,
            "changed_files": [],
            "validators": "UNKNOWN",
            "next_task": "Choose highest-impact safe task from locked Phase-2 objective.",
            "blocker": None,
            "founder_action_needed": False,
            "history": [],
        }


def esc(v):
    s = "" if v is None else str(v)
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def save(doc):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    doc["updated_at"] = now()
    doc["history"] = (doc.get("history") or [])[-20:]
    STATE.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    render(doc)


def record(status, current_task=None, engine=None, changed_files=None, validators=None,
           result=None, next_task=None, blocker=None, founder_action_needed=None):
    doc = load()
    previous_status = doc.get("status")
    if status == "WORKING" and previous_status != "WORKING":
        doc["started_at"] = now()
    if current_task is not None:
        doc["current_task"] = current_task
    if engine is not None:
        doc["ai_engine"] = engine
    if changed_files is not None:
        doc["changed_files"] = list(changed_files)
    if validators is not None:
        doc["validators"] = validators
    if result is not None:
        doc["last_result"] = result
    if next_task is not None:
        doc["next_task"] = next_task
    if blocker is not None or status in {"WORKING", "COMPLETED", "IDLE"}:
        doc["blocker"] = blocker
    if founder_action_needed is not None:
        doc["founder_action_needed"] = bool(founder_action_needed)
    if status == "COMPLETED":
        doc["last_completed"] = doc.get("current_task")
    doc["status"] = status
    doc.setdefault("history", []).append({
        "at": now(), "status": status, "task": doc.get("current_task"),
        "engine": doc.get("ai_engine"), "result": result,
    })
    save(doc)
    return doc


def render(doc=None):
    doc = doc or load()
    files = doc.get("changed_files") or []
    file_html = "<br>".join(esc(x) for x in files) or "None"
    history = "".join(
        f"<tr><td>{esc(h.get('at'))}</td><td>{esc(h.get('status'))}</td><td>{esc(h.get('task'))}</td><td>{esc(h.get('engine'))}</td></tr>"
        for h in reversed((doc.get("history") or [])[-10:])
    ) or '<tr><td colspan="4">No activity yet.</td></tr>'
    founder = "YES" if doc.get("founder_action_needed") else "NO"
    html = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RIO Work Dashboard</title><style>
body{{font-family:system-ui;margin:0;background:#f5f5f5;color:#161616}}main{{max-width:1120px;margin:auto;padding:28px}}h1{{margin-bottom:4px}}.sub{{color:#555}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin:24px 0}}.card,.panel{{background:#fff;padding:18px;border:1px solid #ddd;border-radius:12px}}.card span{{display:block;color:#666;font-size:13px;margin-bottom:6px}}.card strong{{font-size:20px}}.panel{{margin:16px 0;overflow:auto}}table{{width:100%;border-collapse:collapse;font-size:14px}}th,td{{padding:10px;border-bottom:1px solid #eee;text-align:left;vertical-align:top}}.badge{{display:inline-block;padding:6px 10px;border:1px solid #bbb;border-radius:999px;font-weight:700}}</style></head><body><main>
<h1>RIO Operational Dashboard</h1><p class="sub">Live work tracker · Phase 2 autonomous execution</p><span class="badge">{esc(doc.get('status','UNKNOWN'))}</span>
<div class="grid">
<section class="card"><span>Current task</span><strong>{esc(doc.get('current_task'))}</strong></section>
<section class="card"><span>AI engine</span><strong>{esc(doc.get('ai_engine'))}</strong></section>
<section class="card"><span>Validators</span><strong>{esc(doc.get('validators'))}</strong></section>
<section class="card"><span>Founder action needed</span><strong>{founder}</strong></section>
</div>
<section class="panel"><h2>Execution</h2><p><b>Started:</b> {esc(doc.get('started_at'))}</p><p><b>Last completed:</b> {esc(doc.get('last_completed'))}</p><p><b>Result:</b> {esc(doc.get('last_result'))}</p><p><b>Changed files:</b><br>{file_html}</p></section>
<section class="panel"><h2>What happens next</h2><p><b>Next task:</b> {esc(doc.get('next_task'))}</p><p><b>Blocker:</b> {esc(doc.get('blocker') or 'None')}</p><p><b>Last updated:</b> {esc(doc.get('updated_at'))}</p></section>
<section class="panel"><h2>Recent RIO activity</h2><table><tr><th>Time</th><th>Status</th><th>Task</th><th>AI</th></tr>{history}</table></section>
</main></body></html>'''
    for dash in (SITE_DASH, PUBLIC_DASH):
        dash.parent.mkdir(parents=True, exist_ok=True)
        dash.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    render()
    print(PUBLIC_DASH)
