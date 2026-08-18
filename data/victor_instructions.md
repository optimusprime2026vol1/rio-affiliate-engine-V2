# Victor → RIO — instructions

Victor writes here. RIO's operating agent reads this file on every scheduled
run (see RIO_OPERATING_AGENT_BRIEF.md Section 7) and treats new entries as
directives. RIO never writes to this file — status/questions go the other
way, into `data/rio_report_to_victor.md`.

Newest entries first. Format: `## <date> — <OPEN|ACKED> — <short title>`.

---

## 2026-08-18 — OPEN — EarnKaro account created by Vicky — second merchant network ready for integration design

Vicky created and verified the EarnKaro account himself, directly (account
creation and credentials stay founder-only per Section 5 — no agent touched
signup or login). Confirmed logged in and active: **User ID 5551765**,
name "Vickey Gautam", **Total Profit already showing ₹30** — meaning
Amazon.in tracking through EarnKaro is live on this account, independent of
RIO's own Amazon Associates tag (`rioaffiliate-21`).

**Important constraint found while checking the account:** EarnKaro's
dashboard (`My Profile` → `Account Settings`) has no self-serve API key or
token — only Personal Details / Change Password / Language. Their link
conversion is exposed as a manual "paste a product URL → Make Profit Link"
tool at `/create-earn-link`, not a programmatic API. So there is currently
no credential to add as a GitHub secret for this integration — unlike
Zerodha/DeepSeek-style integrations, there's nothing to wire into a script
yet.

**This satisfies the Section 4 phase-plan item** "prepare for a second
merchant network (EarnKaro) — account creation is founder-only." Account
now exists; what's still open is design work, not credential-gathering:

1. Decide how EarnKaro-routed offers get represented in
`data/product_candidates.csv` / `data/offer_identity_registry.csv` (a new
merchant field, presumably — RIO currently assumes Amazon-only identity).
2. Decide the actual workflow for producing EarnKaro links without an API:
most likely a manual conversion step (paste each qualifying offer URL into
EarnKaro's tool) folded into the existing publish pipeline, until/unless
EarnKaro grants bulk/API access on request (that outreach, if pursued,
would also be a Founder-level action, not something the operating agent
can self-serve).
3. Tie back explicitly to the KPI guardrail in Section 4: by month 12, no
single merchant above 30% of approved revenue — EarnKaro (which itself
aggregates Flipkart, Myntra, Ajio, and others beyond Amazon) is the
natural first step toward that diversification, not just a duplicate
Amazon channel.

No code changes made yet, on purpose — this is a status/context entry so
the operating agent has the real account state before designing the
integration on its own initiative. Flagging back to Victor/Founder if the
proposed design in points 1-2 above needs sign-off before implementation.

## 2026-08-17 — OPEN — Distribution push approved: Instagram + Pinterest (organic) + Google AdSense; paid ads explicitly skipped

Vicky wants RIO's traffic pushed harder ("publish ads everywhere"). Clarified
with him directly what that means and what's already true:

**Correction to earlier assumption — the site was already further along than
`README.md` said.** Verified live: https://vickykenin-lang.github.io/rio-affiliate-engine/
is public, has 27 articles, and real Amazon.in affiliate links with
`tag=rioaffiliate-21` are live and working (spot-checked 4 articles across
different categories — kitchen, bathroom, storage, wardrobe). robots.txt,
sitemap.xml and meta robots are all indexing-clean, no SEO blocker found.
`README.md`'s "Public deployment: not activated" line was stale — corrected
it to reflect reality and logged Vicky's explicit 2026-08-17 go-ahead for
public deployment directly in the README's Current Status / Publication
Gate sections.

**Decided, in priority order:**
1. Organic — **Instagram** and **Pinterest** business accounts for RIO's
brand (separate from AURA's own IG/Pinterest — do not reuse AURA's
accounts or tokens for RIO content).
2. **Google AdSense** — display-ad monetization on the site itself (on top
of, not instead of, Amazon affiliate revenue). This is Vicky's own
addition, not something Victor suggested — noting that explicitly since
it's a new revenue-mechanism decision, not routine execution.
3. **Paid ads (Google Ads/Meta Ads) — explicitly SKIPPED for now**, Vicky's
own choice ("Abhi paid ads skip karo"). Do not start any paid-ads work
until he raises it again with an explicit budget.

**Blocked on Vicky (account creation + credentials — cannot be done by an
operating agent or by Victor, per Section 5's non-negotiables):**
- Instagram Business account for RIO's brand, converted/linked to a Facebook
Page, then a Meta for Developers app → long-lived Page Access Token + the
Instagram Business Account ID. Needed as GitHub secrets on
`rio-affiliate-engine`: `IG_USER_ID_RIO`, `IG_ACCESS_TOKEN_RIO` (named
distinctly from AURA's `IG_USER_ID`/`IG_ACCESS_TOKEN` — different brand,
do not collide).
- Pinterest Business account for RIO's brand, verify the site URL, create a
board, then Pinterest Developers → app → access token. Needed as secrets:
`PIN_ACCESS_TOKEN_RIO`, `PIN_BOARD_ID_RIO`.
- Google AdSense signup at adsense.google.com with the RIO site URL —
requires Vicky's own tax/payment details, Victor/RIO cannot enter these.
Approval can take days. Once approved, the AdSense publisher ID
(`ca-pub-...`) is needed to add the ad script to the site template.

**Once any of these secrets/IDs exist**, tell Victor and the corresponding
piece gets built the same way DeepSeek/Cloudflare were added to AURA:
a social-publishing script (content source = `data/content_queue.csv` +
`data/offer_identity_registry.csv`, since RIO has no calendar.json
equivalent — this itself is new design work, not a copy-paste of AURA's
publisher.py) for IG/Pinterest, and an AdSense script tag injected into the
site build for the display-ad piece. Neither has been built yet — no
accounts exist yet to build against.

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
