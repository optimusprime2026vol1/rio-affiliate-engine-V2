#!/usr/bin/env python3
"""RIO — Telegram conversation agent (LOCKED).

DeepSeek is PRIMARY. Grok is fallback only after credits exist.
Polls every 5 minutes via GitHub Actions. No manual intervention required.

LOCKED 2026-08-23 by Founder order: no further changes from prior chat agent.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

ROOT = os.path.join(os.path.dirname(__file__), "..")
IST = timezone(timedelta(hours=5, minutes=30))
STATE_PATH = os.path.join(ROOT, "data", "telegram_chat_state.json")
STATUS_PATH = os.path.join(ROOT, "data", "status.json")
CONTROL_PATH = os.path.join(ROOT, "data", "control.json")

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
GROK_KEY = clean_secret(
    os.environ.get("GROK_API_KEY", "") or os.environ.get("XAI_API_KEY", "")
)


def jload(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def jsave(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)


def tg_api(method, params=None, http_method="GET"):
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN_RIO missing")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    if http_method == "GET":
        if params:
            url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, method="GET")
    else:
        data = urllib.parse.urlencode(params or {}).encode()
        req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def send_message(chat_id, text):
    text = (text or "").strip()
    if not text:
        return False
    if len(text) > MAX_REPLY_CHARS:
        text = text[: MAX_REPLY_CHARS - 20] + "\n\n…(truncated)"
    body = tg_api(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": True,
        },
        http_method="POST",
    )
    return bool(body.get("ok"))


def system_prompt():
    status = jload(STATUS_PATH, {})
    control = jload(CONTROL_PATH, {})
    counts = status.get("counts") or {}
    return (
        "You are RIO, the operating agent for the rio-affiliate-engine affiliate business.\n"
        "Founder is Vicky. Speak as RIO. This Telegram chat is the primary Founder interface.\n"
        "RIO 3.0: help Indian interior designers, contractors, and small offices use AI tools "
        "and practical digital products; supporting layer is verified home/living products.\n"
        "Objective: ₹10 lakh/month net approved commission (12–24 month realistic frame).\n"
        "Non-negotiables: no fabricated prices/ratings/ASINs; no credential/account creation; "
        "no Founder name on public content without explicit approval; revenue stays ₹0 until real.\n"
        "Instagram auto-publish is paused by Founder (old home-storage card style not wanted).\n"
        "Reply in the same language the user uses (Hindi/English mix is fine). Be direct.\n"
        "You cannot push code or change GitHub from this loop — if asked, say what should be done.\n"
        f"Live snapshot (may be minutes old): kill_switch={control.get('kill_switch')}, "
        f"ready_offers={counts.get('ready_offers')}, content_items={counts.get('content_items')}, "
        f"all_validators_pass={status.get('all_validators_pass')}, "
        f"status_updated={status.get('updated')}.\n"
        "If unsure, say so. Do not invent live Amazon prices or earnings."
    )


def build_messages(history, user_text):
    messages = [{"role": "system", "content": system_prompt()}]
    for m in history[-MAX_HISTORY:]:
        role = m.get("role")
        content = (m.get("content") or "").strip()
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": user_text})
    return messages


def call_chat_api(url, key, model, messages):
    payload = {"model": model, "messages": messages, "temperature": 0.5}
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        body = json.load(r)
    choices = body.get("choices") or []
    if not choices:
        raise RuntimeError("no choices in response")
    content = (choices[0].get("message") or {}).get("content") or ""
    content = content.strip()
    if not content:
        raise RuntimeError("empty content")
    return content


def call_llm(history, user_text):
    """DeepSeek PRIMARY. Grok only if DeepSeek fails."""
    messages = build_messages(history, user_text)
    errors = []

    if DEEPSEEK_KEY:
        try:
            return call_chat_api(DEEPSEEK_URL, DEEPSEEK_KEY, DEEPSEEK_MODEL, messages), "deepseek"
        except urllib.error.HTTPError as e:
            err = e.read().decode(errors="replace")
            errors.append(f"deepseek HTTP {e.code}: {err[:200]}")
        except Exception as e:
            errors.append(f"deepseek: {e}")

    if GROK_KEY:
        try:
            return call_chat_api(GROK_URL, GROK_KEY, GROK_MODEL, messages), "grok"
        except urllib.error.HTTPError as e:
            err = e.read().decode(errors="replace")
            errors.append(f"grok HTTP {e.code}: {err[:200]}")
        except Exception as e:
            errors.append(f"grok: {e}")

    if not DEEPSEEK_KEY and not GROK_KEY:
        return (
            "No AI key available (DEEPSEEK_API_KEY / GROK_API_KEY).",
            "none",
        )

    return (
        "RIO temporarily cannot reach AI APIs.\n" + "\n".join(errors[:3]),
        "error",
    )


def allowed_chat(chat):
    if not chat:
        return False
    chat_id = str(chat.get("id", ""))
    chat_type = chat.get("type") or ""
    if chat_type == "private":
        return True
    if ALERT_CHAT_ID and chat_id == str(ALERT_CHAT_ID):
        return True
    return False


def main():
    if not BOT_TOKEN:
        print("[telegram_chat] missing TELEGRAM_BOT_TOKEN_RIO")
        return 2

    state = jload(STATE_PATH, {"offset": 0, "chats": {}, "updated_at": None})
    offset = int(state.get("offset") or 0)

    try:
        updates = tg_api("getUpdates", {"offset": offset, "timeout": 0, "limit": 30})
    except Exception as e:
        print(f"[telegram_chat] getUpdates failed: {e}")
        return 1

    if not updates.get("ok"):
        print(f"[telegram_chat] getUpdates not ok: {updates}")
        return 1

    results = updates.get("result") or []
    handled = 0

    for upd in results:
        update_id = upd.get("update_id")
        if update_id is not None:
            state["offset"] = max(int(state.get("offset") or 0), int(update_id) + 1)

        msg = upd.get("message") or upd.get("edited_message")
        if not msg:
            continue
        chat = msg.get("chat") or {}
        if not allowed_chat(chat):
            continue
        text = (msg.get("text") or "").strip()
        if not text:
            continue
        from_user = msg.get("from") or {}
        if from_user.get("is_bot"):
            continue

        chat_id = str(chat.get("id"))
        chats = state.setdefault("chats", {})
        history = chats.setdefault(chat_id, {}).setdefault("history", [])

        low = text.casefold().strip()
        if low in {"/start", "start"}:
            reply = (
                "RIO online.\n\n"
                "Yahan seedha baat karo.\n"
                "Auto reply har ~5 min.\n\n"
                "Commands: /status"
            )
            engine = "local"
        elif low in {"/status", "status"}:
            status = jload(STATUS_PATH, {})
            counts = status.get("counts") or {}
            control = jload(CONTROL_PATH, {})
            reply = (
                f"Status @ {status.get('updated', '?')}\n"
                f"kill_switch: {control.get('kill_switch')}\n"
                f"validators: {status.get('all_validators_pass')}\n"
                f"ready_offers: {counts.get('ready_offers')}\n"
                f"content_items: {counts.get('content_items')}\n"
                f"IG auto-publish: paused\n"
                f"AI primary: DeepSeek (locked)"
            )
            engine = "local"
        else:
            reply, engine = call_llm(history, text)

        ok = send_message(chat_id, reply)
        print(f"[telegram_chat] chat={chat_id} ok={ok} engine={engine} text={text[:40]!r}")

        history.append({"role": "user", "content": text})
        history.append({"role": "assistant", "content": reply})
        chats[chat_id]["history"] = history[-MAX_HISTORY:]
        chats[chat_id]["last_at"] = datetime.now(IST).isoformat(timespec="minutes")
        chats[chat_id]["last_engine"] = engine
        handled += 1

    state["updated_at"] = datetime.now(IST).isoformat(timespec="minutes")
    jsave(STATE_PATH, state)
    print(f"[telegram_chat] done handled={handled} offset={state.get('offset')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
