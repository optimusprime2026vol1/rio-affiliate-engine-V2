# Victor → RIO — instructions

Victor writes here. RIO's operating agent reads this file on every scheduled
run (see RIO_OPERATING_AGENT_BRIEF.md Section 7) and treats new entries as
directives. RIO never writes to this file — status/questions go the other
way, into `data/rio_report_to_victor.md`.

Newest entries first. Format: `## <date> — <OPEN|ACKED> — <short title>`.

---

## 2026-08-18 — ACKED — AdSense root-domain fix: designinfra.in connected to WordPress, site verified, review requested

Root cause of the earlier "Couldn't verify your site" AdSense error, found
and fixed this run: AdSense's initial site-ownership check needs the root
domain (`designinfra.in`), which was hosted on GoDaddy's own Website
Builder product — a completely separate codebase from `rio.designinfra.in`
(GitHub Pages), which is where the AdSense verification script actually
lived. Adding the script to all 30 RIO site pages (done last run) could
never have worked for root-domain verification because the two domains
weren't even the same website.

**Fix, done with Vicky's explicit go-ahead before touching DNS:** connected
`designinfra.in` to Vicky's existing GoDaddy Managed WordPress site ("RIO
SALLERIOR") via GoDaddy's own domain-connect flow (Settings → Domains →
Add Domain, on the WordPress hosting dashboard) rather than hand-editing
the DNS A record — GoDaddy configures the target IP itself this way.
Confirmed after the switch propagated: `designinfra.in` now resolves to the
WordPress site's IP (`160.153.0.217`) and serves it live; `rio.designinfra.in`
and `docs.designinfra.in` CNAMEs were not touched and still resolve to
`vickykenin-lang.github.io` exactly as before — RIO's actual site and the
AURA dashboard are unaffected.

**AdSense status after this run (Vicky completed the verify/consent steps
himself):** site ownership verified, ad review requested, EEA/UK/Switzerland
consent message configured (Google's own CMP, 2-choice: Consent + Manage
options). Account is now waiting on Google's manual ad-approval review —
no fixed timeline on Google's side, commonly anywhere from a few hours to
~2 weeks. Nothing further to do until Google responds; do not re-submit or
re-verify in the meantime.

**Flagging on purpose, not a bug:** `designinfra.in` is currently a bare/
default WordPress install, not populated with RIO's real content — this
matches Vicky's own explicit scope from this same conversation ("basic
site now, full detail after AdSense is sorted"). Once AdSense approval
comes through, populating this site (or deciding it stays a thin
redirect/landing point while `rio.designinfra.in` remains the real
content site) is the next open decision, not yet made.

## 2026-08-18 — ACKED — Instagram publishing script built and live — auto-publish mode, first run scheduled ~19:00 IST today

Vicky's call, direct: once IG_USER_ID_RIO/IG_ACCESS_TOKEN_RIO existed (see
the entry below), he asked for the Instagram publishing script to be built
now, and chose **fully automatic** publishing (no per-post approval step)
over a manual-review-first option I offered him. Built and pushed this run:

**What's live:**
- `scripts/publish_instagram.py` (new, stdlib-only — no new dependency,
matches heartbeat.py/generate_dashboard.py convention; there is no pip
install step in rio.yml).
- `instagram-publish` job added to `.github/workflows/rio.yml`, scheduled
daily ~19:00 IST (`30 13 * * *` UTC), plus manual `workflow_dispatch`.
- `site/social/*.png` (new, 17 files) — one branded card per currently
READY+ACTIVE+VERIFIED+IN_STOCK offer in `data/offer_identity_registry.csv`.
- `data/ig_published.json` (new) — dedup state so no offer is ever posted
twice; the script always picks the next un-posted eligible offer, one per
run.

**Important blocker found and worked around, on purpose — read before
assuming this posts real product photos:** Amazon.in's robots.txt disallows
scraping product pages, and RIO has no Amazon Product Advertising API
credentials (that would be a separate founder-level signup, not done).
So this script does **not** scrape or fabricate a product photo. Instead
each post uses a pre-rendered branded card (product name + category, pulled
straight from the same verified registry fields — no invented copy) built
by me from a shared HTML template. This satisfies the "no fabricated data"
non-negotiable but means posts are branded cards, not real product
photography, until Amazon PA-API access exists or Vicky supplies real
photos. Flagging this as a real product-quality gap, not hiding it.

**Guardrails built in:**
- Respects the kill switch (`data/control.json`) and the last-known
validator status (`data/status.json.all_validators_pass`) — will not post
if either says stop, same rule as heartbeat.py.
- Every caption includes a plain-language affiliate disclosure
("Affiliate link... #ad #affiliate") — never a bare undisclosed link.
- One post per run only — cadence is controlled entirely by the workflow
schedule, not by the script.
- New offers added to the registry later will have **no** social card until
one is generated for them — the script skips (logs, does not post) any
eligible offer with no matching `site/social/<offer_id>.png`. Generating
cards for future offers is a follow-up task, not yet automated.

Not yet done: Pinterest and Google AdSense are still fully blocked on Vicky
per the 2026-08-17 "Distribution push approved" entry below — this entry
only clears the Instagram-script half of that plan.

## 2026-08-18 — OPEN — Instagram credentials generated — IG_USER_ID_RIO and IG_ACCESS_TOKEN_RIO now live as GitHub secrets

Vicky completed the Meta for Developers app setup for RIO's Instagram Business
account (@riosallerior) himself, directly (account creation, login, and token
generation stay founder-only per Section 5 — no agent touched credentials):

- Meta app "Rio_Sallerior-IG" (App ID 928789399631996), Instagram API product
added, required permissions (`instagram_business_basic`,
`instagram_business_manage_comments`, `instagram_business_manage_messages`,
`instagram_business_content_publish`) already enabled.
- `riosallerior` added as Instagram Tester on the app; invite accepted by
Vicky via Instagram.com web (tester invites do not show in the Instagram
mobile app — only on Instagram.com → Edit Profile → Apps and Websites →
Tester invitations tab).
- Access token generated by Vicky in Meta's own OAuth popup and copied by
him directly — not typed, seen, or handled by any agent, per the hard
credential-handling rule.
- Instagram Business Account ID: **17841435772670647**.
- Both values are now live as GitHub secrets on this repo:
`IG_USER_ID_RIO` = 17841435772670647, `IG_ACCESS_TOKEN_RIO` = (the
generated token — value not reproduced here or anywhere outside GitHub
Secrets).

This clears the Instagram half of the credential-blocker noted in the
2026-08-17 "Distribution push approved" entry below. Pinterest and Google
AdSense credentials are still outstanding (see that entry) — do not treat
this as clearing those.

**Next build step, now unblocked:** the social-publishing script for
Instagram described in that same entry — content source =
`data/content_queue.csv` + `data/offer_identity_registry.csv`, publishing
via the Instagram Content Publishing API using
`IG_USER_ID_RIO`/`IG_ACCESS_TOKEN_RIO`. Not built yet — this is a
status/credential entry only, flagging to Victor that the blocker is
cleared and the build can start.

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
