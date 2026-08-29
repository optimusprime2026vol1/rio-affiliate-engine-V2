#!/usr/bin/env python3
"""Collect real Instagram metrics for every published RIO post.

RIO v1 stalled because engagement_tracking stayed null forever, so the
condition "if no clicks within 24h" was always true and the engine looped
between A/B tests it could never evaluate. This script is the fix: it pulls
live numbers from the Graph API and writes them into a metrics ledger that
the forecaster and the action selector both read.

Never invents a number. A metric that cannot be fetched stays null and is
recorded as UNAVAILABLE, not as zero.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
API_VERSION = os.environ.get("IG_GRAPH_API_VERSION", "v25.0").strip() or "v25.0"
GRAPH = "https://graph.facebook.com"
TIMEOUT = 45

FEED_METRICS = ["impressions", "reach", "saved", "profile_visits", "website_clicks"]


def load_json(path: str, default):
    try:
        with open(os.path.join(ROOT, path), encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return default


def save_json(path: str, data) -> None:
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def request_json(path: str, token: str, params: dict) -> tuple[dict, str | None]:
    values = {**params, "access_token": token}
    url = f"{GRAPH}/{API_VERSION}/{path.strip('/')}?{urllib.parse.urlencode(values)}"
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8")), None
    except urllib.error.HTTPError as exc:
        try:
            payload = json.loads(exc.read().decode("utf-8"))
            message = str(payload.get("error", {}).get("message", ""))[:200]
        except Exception:
            message = f"HTTP {exc.code}"
        return {}, message.replace(token, "[REDACTED]")
    except urllib.error.URLError:
        return {}, "network request failed"
    except json.JSONDecodeError:
        return {}, "invalid JSON response"


def fetch_metrics(media_id: str, token: str) -> tuple[dict, list[str]]:
    """Fetch each metric independently so one unsupported metric cannot
    blank out the entire result for that post."""
    values: dict[str, int | None] = {}
    problems: list[str] = []
    for metric in FEED_METRICS:
        payload, error = request_json(f"{media_id}/insights", token, {"metric": metric})
        if error:
            values[metric] = None
            problems.append(f"{metric}: {error}")
            continue
        entries = payload.get("data") or []
        if not entries:
            values[metric] = None
            problems.append(f"{metric}: no data returned")
            continue
        series = entries[0].get("values") or [{}]
        raw = series[0].get("value")
        values[metric] = int(raw) if isinstance(raw, (int, float)) else None
        if values[metric] is None:
            problems.append(f"{metric}: value missing")
    return values, problems


def main() -> int:
    token = os.environ.get("IG_RIO_TOKEN", "").strip()
    if not token:
        print("REFUSED: IG_RIO_TOKEN is required")
        return 1

    published = load_json("data/ig_published.json", {}).get("posted", {})
    if not published:
        print("REFUSED: data/ig_published.json has no posted entries")
        return 1

    ledger = load_json("data/metrics_ledger.json", {"schema_version": 1, "posts": {}})
    ledger.setdefault("posts", {})
    now = datetime.now(timezone.utc).isoformat()

    collected = 0
    unavailable = 0

    for key, entry in published.items():
        media_id = str(entry.get("media_id", "")).strip()
        if not media_id:
            continue
        values, problems = fetch_metrics(media_id, token)
        usable = any(value is not None for value in values.values())
        if usable:
            collected += 1
        else:
            unavailable += 1

        record = ledger["posts"].setdefault(
            key,
            {
                "media_id": media_id,
                "permalink": entry.get("permalink", ""),
                "product_name": entry.get("product_name", ""),
                "posted_at": entry.get("posted_at", ""),
                "history": [],
            },
        )
        record["latest"] = values
        record["latest_status"] = "COLLECTED" if usable else "UNAVAILABLE"
        record["latest_problems"] = problems
        record["last_checked"] = now
        record["history"].append({"at": now, **values})
        record["history"] = record["history"][-60:]

    totals: dict[str, int | None] = {}
    for metric in FEED_METRICS:
        numbers = [
            post["latest"].get(metric)
            for post in ledger["posts"].values()
            if isinstance(post.get("latest", {}).get(metric), int)
        ]
        totals[metric] = sum(numbers) if numbers else None

    ledger["schema_version"] = 1
    ledger["updated_at"] = now
    ledger["totals"] = totals
    ledger["collection_summary"] = {
        "posts_collected": collected,
        "posts_unavailable": unavailable,
        "truth_rule": "A null metric means not measured. It must never be read as zero.",
    }

    save_json("data/metrics_ledger.json", ledger)
    print(
        f"METRICS COLLECTED: {collected} post(s) with data, "
        f"{unavailable} unavailable. Totals: {json.dumps(totals)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
