#!/usr/bin/env python3
"""RIO — Telegram Founder interface.

DeepSeek is PRIMARY; Grok is fallback. Founder messages can now be planned and,
when policy permits, executed through the guarded deterministic executor.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

from rio_autonomous_executor import execute as execute_plan

ROOT = os.path.join(os.path.dirname(__file__), "..")
IST = timezone(timedelta(hours=5, minutes=30))
STATE_PATH = os.path.join(ROOT, "data", "telegram_chat_state.json")
STATUS_PATH = os.path.join(ROOT, "data", "status.json")
CONTROL_PATH = os.path.join(ROOT, "data", "control.json")
CORE_PATH = os.path.join(ROOT, "data", "RIO_3.0_DEFINITION.md")
POLICY_PATH = os.path.join(ROOT, "data", "AUTONOMY_POLICY.md")

DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"
GROK_URL = "https://api.x.ai/v1/chat/completions"
GROK_MODEL = "grok-4.6"
MAX_HISTORY = 12
MAX_REPLY_CHARS = 3500


def clean_secret(value):
    value = (value or "").strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1].strip()
    return value

BOT_TOKEN = clean_secret(os.environ.get("TELEGRAM_BOT_TOKEN_RIO", ""))
ALERT_CHAT_ID = clean_secret(os.environ.get("TELEGRAM_CHAT_ID_RIO", ""))
DEEPSEEK_KEY = clean_secret(os.environ.get("DEEPSEEK_API_KEY", ""))
GROK_KEY = clean_secret(os.environ.get("GROK_API_KEY", "") or os.environ.get("XAI_API_KEY", ""))


def jload(path, default):
    try:
        with open(path, encoding="utf-8") as f: return json.load(f)
    except Exception: return default


def read_text(path, limit=14000):
    try:
        with open(path, encoding="utf-8") as f: return f.read()[:limit]
    except Exception: return ""


def jsave(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: json.dump(obj, f, indent=1, ensure_ascii=False)


def tg_api(method, params=None, http_method="GET"):
    if not BOT_TOKEN: raise RuntimeError("TELEGRAM_BOT_TOKEN_RIO missing")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    if http_method == "GET":
        if params: url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, method="GET")
    else:
        req = urllib.request.Request(url, data=urllib.parse.urlencode(params or {}).encode(), method="POST")
    with urllib.request.urlopen(req, timeout=60) as r: return json.load(r)


def send_message(chat_id, text):
    text = (text or "").strip()
    if not text: return False
    if len(text) > MAX_REPLY_CHARS: text = text[:MAX_REPLY_CHARS-20] + "\n\n…(truncated)"
    body = tg_api("sendMessage", {"chat_id": chat_id, "text": text, "disable_web_page_preview": True}, "POST")
    return bool(body.get("ok"))


def system_prompt():
    status, control = jload(STATUS_PATH, {}), jload(CONTROL_PATH, {})
    counts = status.get("counts") or {}
    core, policy = read_text(CORE_PATH), read_text(POLICY_PATH)
    return f"""You are RIO, autonomous operating agent for rio-affiliate-engine. Founder is Vicky.
Telegram is the Founder command interface. DeepSeek is primary operating intelligence.
Your job is not only to advise: when Founder explicitly asks for a safe system/content/data change, create an execution plan.

SOURCE OF TRUTH — RIO CORE:\n{core}\n
AUTONOMY POLICY:\n{policy}\n
Live snapshot: kill_switch={control.get('kill_switch')}; ready_offers={counts.get('ready_offers')}; content_items={counts.get('content_items')}; validators={status.get('all_validators_pass')}; updated={status.get('updated')}.

Return ONLY valid JSON, no markdown fences, with this schema:
{{"intent":"respond|execute","summary":"...","risk":"low|medium|high","operations":[],"founder_message":"..."}}
For operations use only:
{{"op":"write_text","path":"data/... or site/... or scripts/...","content":"complete content"}}
{{"op":"write_json","path":"data/...","value":{{}}}}
{{"op":"append_text","path":"data/...","content":"..."}}
Never request arbitrary shell execution. Never modify protected files. Never put credentials/secrets in files.
If request needs credentials/account/payment/legal action or protected core/workflow change, intent=respond, risk=high and clearly say VICKY ACTION REQUIRED.
If user is simply chatting/asking status/advice, intent=respond and operations=[]. Reply in user's language.
"""


def build_messages(history, user_text):
    messages = [{"role":"system","content":system_prompt()}]
    for m in history[-MAX_HISTORY:]:
        if m.get("role") in ("user","assistant") and (m.get("content") or "").strip(): messages.append(m)
    messages.append({"role":"user","content":user_text})
    return messages


def call_chat_api(url, key, model, messages):
    data = json.dumps({"model":model,"messages":messages,"temperature":0.2}).encode()
    req = urllib.request.Request(url, data=data, method="POST", headers={"Content-Type":"application/json","Authorization":f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=90) as r: body=json.load(r)
    content=((body.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
    if not content.strip(): raise RuntimeError("empty content")
    return content.strip()


def parse_plan(raw):
    text=raw.strip()
    if text.startswith("```"):
        text=text.strip("`")
        if text.lstrip().startswith("json"): text=text.lstrip()[4:].lstrip()
    obj=json.loads(text)
    if not isinstance(obj,dict): raise ValueError("plan is not object")
    return obj


def call_llm(history,user_text):
    messages=build_messages(history,user_text); errors=[]
    for name,url,key,model in [("deepseek",DEEPSEEK_URL,DEEPSEEK_KEY,DEEPSEEK_MODEL),("grok",GROK_URL,GROK_KEY,GROK_MODEL)]:
        if not key: continue
        try: return parse_plan(call_chat_api(url,key,model,messages)),name
        except urllib.error.HTTPError as e: errors.append(f"{name} HTTP {e.code}: {e.read().decode(errors='replace')[:200]}")
        except Exception as e: errors.append(f"{name}: {e}")
    return {"intent":"respond","risk":"high","operations":[],"founder_message":"RIO AI unavailable. " + " | ".join(errors[:2])},"error"


def allowed_chat(chat):
    if not chat: return False
    chat_id=str(chat.get("id","")); chat_type=chat.get("type") or ""
    # For autonomous execution, only the configured Founder chat is trusted when configured.
    if ALERT_CHAT_ID: return chat_id == str(ALERT_CHAT_ID)
    return chat_type == "private"


def status_reply():
    status,control=jload(STATUS_PATH,{}),jload(CONTROL_PATH,{})
    counts=status.get("counts") or {}
    return (f"Status @ {status.get('updated','?')}\nkill_switch: {control.get('kill_switch')}\nvalidators: {status.get('all_validators_pass')}\nready_offers: {counts.get('ready_offers')}\ncontent_items: {counts.get('content_items')}\nIG auto-publish: {control.get('instagram_auto_publish')}\nAI primary: DeepSeek\nautonomous executor: ACTIVE")


def main():
    if not BOT_TOKEN: print("[telegram_chat] missing TELEGRAM_BOT_TOKEN_RIO"); return 2
    state=jload(STATE_PATH,{"offset":0,"chats":{},"updated_at":None}); offset=int(state.get("offset") or 0)
    try: updates=tg_api("getUpdates",{"offset":offset,"timeout":0,"limit":30})
    except Exception as e: print(f"[telegram_chat] getUpdates failed: {e}"); return 1
    if not updates.get("ok"): return 1
    handled=0
    for upd in updates.get("result") or []:
        uid=upd.get("update_id")
        if uid is not None: state["offset"]=max(int(state.get("offset") or 0),int(uid)+1)
        msg=upd.get("message") or upd.get("edited_message")
        if not msg or not allowed_chat(msg.get("chat") or {}): continue
        text=(msg.get("text") or "").strip(); from_user=msg.get("from") or {}
        if not text or from_user.get("is_bot"): continue
        chat_id=str((msg.get("chat") or {}).get("id")); chats=state.setdefault("chats",{}); history=chats.setdefault(chat_id,{}).setdefault("history",[])
        low=text.casefold().strip()
        if low in {"/start","start"}: reply="RIO online. DeepSeek primary. Autonomous guarded executor ACTIVE. Commands: /status"; engine="local"
        elif low in {"/status","status"}: reply=status_reply(); engine="local"
        else:
            plan,engine=call_llm(history,text)
            if plan.get("intent")=="execute":
                result=execute_plan(plan,request_summary=text,engine=engine)
                base=(plan.get("founder_message") or plan.get("summary") or "Execution processed.").strip()
                changed=", ".join(result.get("changed_paths") or [])
                if result.get("ok"):
                    reply=f"✅ COMPLETED\n{base}" + (f"\nChanged: {changed}" if changed else "") + "\nValidators: PASS"
                else:
                    reply=f"⚠️ {result.get('status','FAILED')}\n{base}\nBlocker/Error: {result.get('error','unknown')}"
            else: reply=(plan.get("founder_message") or plan.get("summary") or "RIO received your message.").strip()
        ok=send_message(chat_id,reply); print(f"[telegram_chat] chat={chat_id} ok={ok} engine={engine} text={text[:40]!r}")
        history.append({"role":"user","content":text}); history.append({"role":"assistant","content":reply}); chats[chat_id]["history"]=history[-MAX_HISTORY:]
        chats[chat_id]["last_at"]=datetime.now(IST).isoformat(timespec="minutes"); chats[chat_id]["last_engine"]=engine; handled+=1
    state["updated_at"]=datetime.now(IST).isoformat(timespec="minutes"); jsave(STATE_PATH,state)
    print(f"[telegram_chat] done handled={handled} offset={state.get('offset')}"); return 0

if __name__=="__main__": sys.exit(main())
