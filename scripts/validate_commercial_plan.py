#!/usr/bin/env python3
"""Fail-closed validation for the Founder-locked RIO commercial plan."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "COMMERCIAL_VALIDATION_POLICY.json"
DEFINITION = ROOT / "data" / "RIO_3.0_DEFINITION.md"


def main():
    errors = []
    try:
        policy = json.loads(POLICY.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"COMMERCIAL PLAN GATE: FAIL; policy unreadable: {exc}")
        return 1
    definition = DEFINITION.read_text(encoding="utf-8") if DEFINITION.exists() else ""
    timeline = policy.get("timeline") or {}
    expected = {
        "execution_validation_days": [1, 30],
        "organic_market_validation_days": [31, 60],
        "commercial_validation_days": [61, 90],
        "day_30_decision_scope": "EXECUTION_READINESS_NOT_FINAL_ORGANIC_VIABILITY",
    }
    for key, value in expected.items():
        if timeline.get(key) != value:
            errors.append(f"timeline.{key} must equal {value!r}")
    if (policy.get("compliance_gate") or {}).get("type") != "HARD_PASS_FAIL":
        errors.append("compliance gate must be HARD_PASS_FAIL")
    if policy.get("conversion_sensitivity_rates") != [0.005, 0.01, 0.02, 0.03]:
        errors.append("conversion sensitivity must include 0.5%, 1%, 2%, 3%")
    if policy.get("failed_pilot_limit_before_strategy_review") != 2:
        errors.append("strategy review must be mandatory after two failed pilots")
    if policy.get("score_10_rule") != "PREDECLARED_PAID_SETTLEMENT_OBJECTIVE_WITH_COMPLETE_EVIDENCE":
        errors.append("score 10 evidence rule missing")
    markers = (
        "## 2A. Commercial Validation Policy — FOUNDER LOCKED (2026-08-28)",
        "Day 30 judges execution readiness, not final organic viability",
        "Compliance is a **hard pass/fail gate**",
        "two consecutive failed niche pilots",
        "### Weekly evidence contract",
    )
    for marker in markers:
        if marker not in definition:
            errors.append(f"canonical definition missing marker: {marker}")
    if errors:
        print("COMMERCIAL PLAN GATE: FAIL")
        for error in errors:
            print("-", error)
        return 1
    print("COMMERCIAL PLAN GATE: PASS; RIO_COMMERCIAL_VALIDATION_V2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
