# Victor → RIO — instructions

Victor writes here. RIO's operating agent reads this file on every scheduled
run (see RIO_OPERATING_AGENT_BRIEF.md Section 7) and treats new entries as
directives. RIO never writes to this file — status/questions go the other
way, into `data/rio_report_to_victor.md`.

Newest entries first. Format: `## <date> — <OPEN|ACKED> — <short title>`.

---

## 2026-08-17 — ACKED — Scope decision: governance layer is the deadline deliverable; product-discovery AI picked for later

Vicky's call, direct: for the "finalize RIO by tomorrow evening" deadline,
**scope is the governance layer only** (heartbeat, kill switch, dashboard
auto-refresh, this mailbox) — already built and live-verified as of this
entry (see run history on `.github/workflows/rio.yml`, first manual run
passed all 4 validators). Product discovery / live-verification / content
drafting automation is explicitly OUT of this deadline — treat it as a
separate future build, not a "kal evening" blocker.

When that future build starts: **DeepSeek** is the pre-approved choice for
RIO's product-discovery/content AI (same reasoning as AURA's
`business_review.py` — already a proven working integration, reuse the
pattern: `DEEPSEEK_API_KEY` as a GitHub secret, an OpenAI-compatible REST
client). No key has been added to this repo yet — that still needs Vicky to
add `DEEPSEEK_API_KEY` as a secret on `rio-affiliate-engine` (can be the
same key already on `design-infra-marketing`, or a fresh one) before that
build can start. Do not begin the discovery/verification script until that
secret exists and Victor confirms go-ahead.

## 2026-08-17 — ACKED — Heartbeat automation is now live; start the operating loop

RIO had zero automation beyond the push-triggered `deploy-pages.yml` static
deploy — no issue listener, no kill switch, no recurring dashboard refresh.
That gap is now closed:

- `scripts/heartbeat.py` (new) — reads open GitHub issues for `KILL SWITCH`
  / `RESUME RIO` / `MESSAGE TO RIO`, regenerates the dashboard
  (`scripts/generate_dashboard.py`), runs all four validators
  (`validate_offer_integrity.py`, `validate_product_candidates.py`,
  `validate_dashboard.py`, `validate_production_offer_gate.py`), and writes
  a fresh `data/status.json` every run.
- `.github/workflows/rio.yml` (new) — runs the heartbeat every 30 minutes,
  on any opened issue, and on manual dispatch.
- `data/control.json`, `data/inbox.json` (new) — kill-switch state and the
  owner-message inbox, same pattern as design-infra-marketing (AURA).
- `data/status.json` — will be written by the first heartbeat run;
  contains `updated` (IST timestamp), `validators` (pass/fail per gate),
  and `counts` (pulled straight from `data/dashboard_snapshot.json`, never
  inferred).

**What this does NOT do yet, on purpose:** it does not do product
discovery, live-verification, or content drafting — RIO has no script for
any of that today (only validators + the dashboard generator existed
before this). That is a separate, larger build and needs a decision on
which AI/API powers it (see the open question below) before I build
anything around it — no API key has been added for RIO yet, unlike
DEEPSEEK_API_KEY/CLOUDFLARE_* on AURA.

**Open question for the Founder, routed via this file per the brief's
Section 7 escalation rule:** which AI should be RIO's actual content/product
research engine (ChatGPT was mentioned informally; Gemini and DeepSeek are
already proven working integrations on AURA and could be reused here with
the same API-key-as-GitHub-secret pattern)? Once decided, tell Victor and
he will wire the client + a discovery/verification script the same way
DeepSeek was added to AURA.

Please run the four verification steps in Section 0 of
`RIO_OPERATING_AGENT_BRIEF.md` before relying on any status this file or
`data/status.json` reports.
