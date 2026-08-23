#!/usr/bin/env python3
"""RIO — Telegram notifier.

Sends status / alert messages to the Founder channel configured via
GitHub secrets TELEGRAM_BOT_TOKEN_RIO and TELEGRAM_CHAT_ID_RIO.

Usage:
  python scripts/telegram_notify.py "message text"
  python scripts/telegram_notify.py --test

Designed for stdlib only (urllib) so it runs in existing GitHub Actions
without extra dependencies. Never logs the token.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))


def clean_secret(value):
    value = (value or "").strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1].strip()
    return value


def send_telegram(text, parse_mode=None):
    token = clean_secret(os.environ.get("TELEGRAM_BOT_TOKEN_RIO", ""))
    chat_id = clean_secret(os.environ.get("TELEGRAM_CHAT_ID_RIO", ""))

    if not token or not chat_id:
        print("[telegram] BLOCKED: TELEGRAM_BOT_TOKEN_RIO or TELEGRAM_CHAT_ID_RIO missing")
        return False, "missing secrets"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": True,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode

    data = urllib.parse.urlencode(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = json.load(r)
        if body.get("ok"):
            print("[telegram] message sent")
            return True, "sent"
        print(f"[telegram] API not ok: {body}")
        return False, str(body)
    except urllib.error.HTTPError as e:
        err = e.read().decode(errors="replace")
        print(f"[telegram] HTTP {e.code}: {err}")
        return False, err
    except Exception as e:
        print(f"[telegram] error: {e}")
        return False, str(e)


def main():
    if len(sys.argv) < 2:
        print("Usage: telegram_notify.py \"message\" | --test")
        return 2

    if sys.argv[1] == "--test":
        now = datetime.now(IST).strftime("%Y-%m-%d %H:%M IST")
        msg = (
            "RIO Telegram connected.\n\n"
            f"Time: {now}\n"
            "Channel: RIO Alerts\n"
            "Status: Bot + secrets working.\n\n"
            "Next: status alerts and deal drops can use this channel.\n"
            "Instagram auto-publish is currently paused (Founder request)."
        )
        ok, detail = send_telegram(msg)
        return 0 if ok else 1

    text = " ".join(sys.argv[1:]).strip()
    if not text:
        print("[telegram] empty message")
        return 2
    ok, detail = send_telegram(text)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
