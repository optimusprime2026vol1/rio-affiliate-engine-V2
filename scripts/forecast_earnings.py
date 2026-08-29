#!/usr/bin/env python3
"""Forecast RIO earnings from measured funnel data.

The forecast is deliberately refusable. If the funnel has not been measured,
this script does not produce a number - it produces INSUFFICIENT_DATA and
says exactly which input is missing. A forecast built on assumed traffic is
worse than no forecast, because it becomes a target that hides the fact that
nothing has been observed.

Conversion sensitivity is modelled at 0.5%, 1%, 2% and 3% because RIO's
Founder-locked commercial validation amendment requires all four bands, not
just the optimistic one.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONVERSION_BANDS = [0.005, 0.01, 0.02, 0.03]
TARGET_MONTHLY_INR = 1_000_000


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


def measured_clicks(ledger: dict) -> tuple[int | None, list[str]]:
    """Sum website clicks across posts. Returns None when nothing measured."""
    notes: list[str] = []
    posts = ledger.get("posts", {})
    if not posts:
        return None, ["metrics ledger has no posts"]
    values = []
    for key, post in posts.items():
        clicks = post.get("latest", {}).get("website_clicks")
        if isinstance(clicks, int):
            values.append(clicks)
        else:
            notes.append(f"{key}: website_clicks not measured")
    if not values:
        return None, notes or ["no post has a measured website_clicks value"]
    return sum(values), notes


def build_forecast(clicks: int, aov: float, rate: float, days: int) -> dict:
    """Project monthly earnings from a measured click volume."""
    monthly_clicks = clicks * (30.0 / days) if days else 0.0
    projections = {}
    for band in CONVERSION_BANDS:
        orders = monthly_clicks * band
        gross = orders * aov
        commission = gross * rate
        projections[f"{band * 100:g}%"] = {
            "monthly_orders": round(orders, 2),
            "monthly_gross_inr": round(gross, 2),
            "monthly_commission_inr": round(commission, 2),
            "months_to_target_at_this_rate": (
                round(TARGET_MONTHLY_INR / commission, 1) if commission > 0 else None
            ),
        }
    return projections


def main() -> int:
    ledger = load_json("data/metrics_ledger.json", {})
    economics = load_json("data/unit_economics.json", {})
    now = datetime.now(timezone.utc).isoformat()

    aov = economics.get("average_order_value_inr")
    rate = economics.get("commission_rate")
    window_days = economics.get("measurement_window_days", 7)

    blockers: list[str] = []
    clicks, notes = measured_clicks(ledger)

    if clicks is None:
        blockers.append("MEASURED_CLICKS_MISSING")
    if not isinstance(aov, (int, float)) or aov <= 0:
        blockers.append("AVERAGE_ORDER_VALUE_MISSING")
    if not isinstance(rate, (int, float)) or rate <= 0:
        blockers.append("COMMISSION_RATE_MISSING")

    if blockers:
        forecast = {
            "schema_version": 1,
            "generated_at": now,
            "verdict": "INSUFFICIENT_DATA",
            "forecast_inr": None,
            "blockers": blockers,
            "notes": notes,
            "truth_rule": (
                "No earnings forecast is produced until the funnel is measured. "
                "An assumed forecast is not evidence and must not be reported as one."
            ),
            "required_next_action": (
                "Run scripts/collect_instagram_insights.py to measure clicks, and "
                "record average_order_value_inr and commission_rate in "
                "data/unit_economics.json from the Amazon Associates programme."
            ),
        }
        save_json("data/earnings_forecast.json", forecast)
        print(f"INSUFFICIENT_DATA: {', '.join(blockers)}")
        return 0

    projections = build_forecast(int(clicks), float(aov), float(rate), int(window_days))
    forecast = {
        "schema_version": 1,
        "generated_at": now,
        "verdict": "MODELLED_FROM_MEASURED_CLICKS",
        "inputs": {
            "measured_clicks": clicks,
            "measurement_window_days": window_days,
            "average_order_value_inr": aov,
            "commission_rate": rate,
            "input_provenance": "clicks measured via Graph API; AOV and rate from Founder-recorded unit economics",
        },
        "projections_by_conversion_rate": projections,
        "target_monthly_inr": TARGET_MONTHLY_INR,
        "notes": notes,
        "truth_rule": (
            "This is a projection from measured clicks, not earned revenue. "
            "Collected revenue stays at zero until an Amazon Associates approved "
            "commission is recorded in data/revenue_ledger.json."
        ),
    }
    save_json("data/earnings_forecast.json", forecast)
    print(f"FORECAST WRITTEN from {clicks} measured clicks across 4 conversion bands")
    return 0


if __name__ == "__main__":
    sys.exit(main())
