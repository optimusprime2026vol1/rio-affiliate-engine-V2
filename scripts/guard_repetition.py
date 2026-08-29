#!/usr/bin/env python3
"""Detect and block the work loop that trapped RIO v1.

On 29 August 2026 RIO v1 ran eight cycles in forty-five minutes and produced
the same buying guide four times under four different task descriptions, then
settled into a monitoring task whose exit condition it could never evaluate.
No rule existed to notice this.

This guard runs before the action selector. It answers two questions:
  1. Has substantially this task already been done recently?
  2. Is the engine waiting on a condition it has no way to observe?

A blocked task is not a failure. It is the engine being told to go and do
something it has not already done.
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPEAT_THRESHOLD = 2
LOOKBACK_HOURS = 24
SIMILARITY = 0.72

STOPWORDS = {
    "the", "a", "an", "and", "or", "to", "for", "of", "with", "on", "in", "at",
    "is", "are", "then", "after", "this", "that", "it", "as", "by", "from",
}


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


def tokens(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    return {word for word in words if word not in STOPWORDS and len(word) > 2}


def similarity(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def parse_time(value: str):
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def recent_entries(history: list[dict], hours: int) -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    out = []
    for entry in history:
        moment = parse_time(entry.get("at", ""))
        if moment is None:
            continue
        if moment.tzinfo is None:
            moment = moment.replace(tzinfo=timezone.utc)
        if moment >= cutoff:
            out.append(entry)
    return out


def unobservable_condition(task: str, ledger: dict) -> str | None:
    """A task that waits on clicks is unobservable until clicks are measured."""
    lowered = (task or "").lower()
    waits_on_clicks = any(
        phrase in lowered
        for phrase in ("no clicks", "clicks within", "monitor", "engagement")
    )
    if not waits_on_clicks:
        return None
    posts = ledger.get("posts", {})
    measured = any(
        isinstance(post.get("latest", {}).get("website_clicks"), int)
        for post in posts.values()
    )
    if measured:
        return None
    return (
        "Task waits on click data, but no post has a measured website_clicks "
        "value. Run scripts/collect_instagram_insights.py first, otherwise this "
        "condition can never become false."
    )


def main() -> int:
    proposed = os.environ.get("PROPOSED_TASK", "").strip()
    if not proposed:
        status = load_json("data/rio_work_status.json", {})
        proposed = str(status.get("next_task", "")).strip()
    if not proposed:
        print("REFUSED: no proposed task to evaluate")
        return 1

    status = load_json("data/rio_work_status.json", {})
    ledger = load_json("data/metrics_ledger.json", {})
    history = recent_entries(status.get("history", []), LOOKBACK_HOURS)

    matches = []
    for entry in history:
        score = similarity(proposed, entry.get("task", ""))
        if score >= SIMILARITY:
            matches.append({"at": entry.get("at"), "task": entry.get("task"), "similarity": round(score, 3)})

    blocked = len(matches) >= REPEAT_THRESHOLD
    unobservable = unobservable_condition(proposed, ledger)

    verdict = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "proposed_task": proposed,
        "lookback_hours": LOOKBACK_HOURS,
        "similar_recent_tasks": matches,
        "repetition_blocked": blocked,
        "unobservable_condition": unobservable,
        "allowed": not blocked and unobservable is None,
    }

    reasons = []
    if blocked:
        reasons.append(
            f"REPETITION: {len(matches)} substantially similar task(s) in the last "
            f"{LOOKBACK_HOURS}h. Pick a materially different action."
        )
    if unobservable:
        reasons.append(f"UNOBSERVABLE: {unobservable}")
    verdict["reasons"] = reasons

    save_json("data/repetition_guard.json", verdict)

    if verdict["allowed"]:
        print("ALLOWED: task is not a repeat and its exit condition is observable")
        return 0
    for reason in reasons:
        print(f"BLOCKED: {reason}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
