#!/usr/bin/env python3
"""RIO — shared DeepSeek REST client (OpenAI-compatible endpoint, no SDK needed).
Same pattern as design-infra-marketing/scripts/deepseek_client.py (AURA) —
copied deliberately rather than shared, since these are two separate repos.

Needs DEEPSEEK_API_KEY as an env var / GitHub Secret. Fails open (raises,
caller decides) on any error — content_review.py must not let one failed
call take down the whole run.
"""
import json, os, urllib.error, urllib.request

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
API_BASE = os.environ.get("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")


def available():
    return bool(API_KEY)


def ask(prompt, timeout=45):
    if not API_KEY:
        raise RuntimeError("DEEPSEEK_API_KEY not set")
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 700,
    }).encode()
    req = urllib.request.Request(
        f"{API_BASE}/chat/completions", data=body, method="POST",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        try:
            detail = e.read().decode(errors="replace")[:300]
        except Exception:
            detail = "(could not read error body)"
        raise RuntimeError(f"HTTP {e.code} from DeepSeek: {detail}") from e
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
        raise RuntimeError(f"Network error from DeepSeek: {e}") from e
    return data["choices"][0]["message"]["content"]


def ask_json(prompt, timeout=45):
    """Same as ask(), but strips markdown fences and parses JSON. Raises on failure."""
    txt = ask(prompt, timeout).strip()
    if txt.startswith("```"):
        txt = txt.strip("`")
        if txt.lower().startswith("json"):
            txt = txt[4:]
    txt = txt.strip()
    try:
        return json.loads(txt, strict=False)
    except json.JSONDecodeError:
        start, end = txt.find("{"), txt.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(txt[start:end + 1], strict=False)
        raise
