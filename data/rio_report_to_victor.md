# RIO → Victor — status reports

RIO's operating agent writes here, append-only, dated entries (newest first
below the header). Victor writes only to `data/victor_instructions.md` —
never edits this file. See RIO_OPERATING_AGENT_BRIEF.md Section 7 for the
full protocol, including the four-step anti-hallucination verification RIO
must do before its very first entry.

---

## 2026-08-23 — Founder final direction: stop this chat, move to Telegram, Grok API autonomous

**Founder instruction (direct):**
- Do not continue conversation in this chat window.
- Remaining work will be done by the API; main agent decides as per objective.
- Grok API will run everything itself.
- All further communication shifts to Telegram.

**Current state against this direction:**
- Telegram integration for RIO does **not** exist yet. Only a content-format draft (`data/TELEGRAM_DEAL_DROP_FORMAT.md`) exists. No bot, no channel automation, no messaging layer.
- Channel / bot creation is Founder-only (Section 5 non-negotiable).
- Kill switch is still **ON**.
- Instagram token is still invalid.
- No Grok API key is present as a GitHub secret on this repo (DeepSeek key exists and is used by content-review + discovery scripts).

**What Founder must provide before the requested shift can happen:**
1. Create Telegram bot + channel (or group) himself.
2. Add as GitHub secrets (names suggested):
   - `TELEGRAM_BOT_TOKEN_RIO`
   - `TELEGRAM_CHAT_ID_RIO` (or channel ID)
3. If Grok is to be the autonomous decision engine: add `GROK_API_KEY` (or equivalent xAI key) as a GitHub secret.
4. Explicit resume instruction (kill switch OFF) when ready for production actions to resume.

Until the above secrets + resume exist, RIO cannot open a Telegram communication channel or run a Grok-driven autonomous loop. Operating agent will not continue this chat window as instructed.

No credentials touched. No accounts created. No unilateral changes to kill switch.

## 2026-08-23 — Founder direction: full autonomy (except credentials)

**Founder message (paraphrased, direct):** RIO should work on its own agenda without continuous intervention from Founder or operating agent. Update files, design/improve system, chase the objective. Only credential management stays with Founder. If any problem arises → message / escalate clearly. AI API keys can be provided if needed.

### Current reality vs requested autonomy

**Already running unattended (when kill switch is OFF):**
- Heartbeat every 30 min → dashboard + 5 validators
- Daily content-review (DeepSeek)
- Daily product-discovery suggestions (DeepSeek → only DISCOVERY_REQUIRED rows)
- Daily Instagram publish attempt (currently failing)

**Still NOT autonomous:**
1. **Kill switch is currently ON** (Founder-requested pause 2026-08-23). All production actions are paused until explicit resume instruction.
2. **Instagram token invalid** — Graph API returns "Invalid OAuth access token". Requires Founder to regenerate long-lived token and update `IG_ACCESS_TOKEN_RIO` secret.
3. **Live product verification** (real Amazon page check for price/stock/identity) still needs browser or human step — discovery script only ever writes DISCOVERY_REQUIRED.
4. **Content improvement loop does not exist yet** — content_review scores articles (avg 4.6/10) but no script rewrites thin articles automatically.
5. Operating agent itself is chat-driven; the real unattended layer is the GitHub Actions schedule above.

### What is needed for the autonomy Founder described

| Item | Owner | Status |
|------|-------|--------|
| Explicit "resume RIO" / kill switch OFF | Founder | Waiting |
| Fix `IG_ACCESS_TOKEN_RIO` | Founder | Waiting |
| Content-rewrite / improvement script (uses DeepSeek scores) | Operating agent can design + build once kill switch off | Not started |
| Stronger live-verification helper (or accept DISCOVERY_REQUIRED stays manual) | Design decision | Open |
| Clear escalation channel (GitHub issue or report entry) when blocked | Already exists | Working |
| Additional / stronger AI key if wanted for rewrite + discovery | Founder can add | Optional |

**No unilateral action taken.** Kill switch stays ON until Founder says resume. No new credentials touched.

Next action depends on Founder reply to this report.

## 2026-08-23 — Overall System Report (requested)

**Source of truth**: live fetches of `data/status.json` (updated 2026-08-23T14:44+05:30), `data/dashboard_snapshot.json`, `data/control.json`, `data/production_status.json`, `data/content_review_report.json`, `data/instagram_run_status.json`, `data/instagram_approval.json`, `data/ig_published.json`.

### 1. System Health
- **Kill switch**: ON (`true`)
  - Reason: "Founder-requested production pause on 2026-08-23. Resume only after explicit Founder instruction."
- **All validators pass**: `true`
  - production_live: PASS (homepage 200, affiliate tag present, disclosure present, sitemap 200, social card 200)
  - offer_integrity (X→X): PASS
  - product_candidates: PASS
  - dashboard: PASS
  - production_offer_gate: PASS (READY=17)
- **Public site**: LIVE and verified at `https://vickykenin-lang.github.io/rio-affiliate-engine/`
- **Heartbeat**: Last successful run wrote status at 14:44 IST; dashboard regenerated.

### 2. Pipeline Counts (dashboard_snapshot + status)
| Metric | Value |
|--------|-------|
| Product candidates | 35 |
| Ready offers | 17 |
| Blocked offers | 0 |
| Rejected products | 2 |
| Content items / articles | 27 |
| Discovered products | 19 |
| Verified products | 17 |
| X-to-X failures | 0 |
| Revenue (approved) | ₹0 |
| Cost | ₹0 |
| Net profit | ₹0 |

### 3. Content Quality (DeepSeek content_review)
- Articles reviewed this cycle: 23
- Average score: **4.6 / 10**
- Would trust: **13 / 23**
- Recurring weaknesses across many articles:
  - No real price / price range
  - No exact dimensions / measurements
  - No honest cons or limitations
  - No user review excerpts or ratings
  - No comparison vs alternatives
  - Several articles still read as thin placeholders

### 4. Instagram Automation
- Status: **FAILED_RETRY**
- Last attempt: UNDER_SINK_001 at 2026-08-22T23:01+05:30
- Error: Graph API 400 — "Invalid OAuth access token - Cannot parse access token" (code 190)
- Posted count: 0
- `ig_published.json`: empty `{"posted": {}}`
- Approval exists for UNDER_SINK_001 (Founder-approved test), but token is broken.
- **Blocker**: IG_ACCESS_TOKEN_RIO secret is invalid / expired / malformed. Requires Founder to regenerate long-lived token in Meta Developer console and update the GitHub secret.

### 5. Monetisation & Distribution Status
- Amazon Associates tag `rioaffiliate-21` is active at data layer (17 READY offers).
- Live site has affiliate links and disclosure (production_live gate passed).
- EarnKaro account exists (User ID 5551765, already showing ₹30 profit) — integration design still open (no API key available).
- Google AdSense: site ownership verified, ad review requested, waiting on Google. Root domain (`designinfra.in`) fixed to WordPress; RIO content remains on `rio.designinfra.in` / GitHub Pages.
- Pinterest: still blocked on Founder credentials.
- Paid ads: explicitly skipped by Founder.

### 6. Unit Economics (illustrative only)
- Scenario: 10k monthly sessions, 18% CTR, 4% conversion, ₹1800 AOV, 5% commission → ~₹6,480 gross/month.
- Note in file: "Illustrative validation scenario, not a forecast or guarantee."

### 7. Open Items / Blockers (for Victor / Founder)
1. **Kill switch is ON** — all automated publishing and further production actions paused until explicit Founder resume instruction.
2. **Instagram token broken** — regenerate + update `IG_ACCESS_TOKEN_RIO` secret required before any post can succeed.
3. Content quality gap: average 4.6/10 and many articles missing concrete product data (price, dimensions, cons). Strengthening content is the highest-leverage next work once kill switch is lifted.
4. EarnKaro integration design still pending (manual link conversion workflow vs waiting for API).
5. AdSense still in Google review queue.

No new decisions made by the operating agent. All numbers above are live file values, not inferred.

## 2026-08-23 — Section 0 verification

Fetched `https://raw.githubusercontent.com/vickykenin-lang/rio-affiliate-engine/main/data/status.json` directly.

- `"updated"`: `2026-08-23T14:44+05:30`
- `"counts"."ready_offers"`: `17`
- `"counts"."content_items"`: `27`
- `"all_validators_pass"`: `true`

## 2026-08-18 — Section 0 verification (first entry)

Fetched `https://raw.githubusercontent.com/vickykenin-lang/rio-affiliate-engine/main/data/status.json` directly.

- `"updated"`: `2026-08-18T10:51+05:30`
- `"counts"."ready_offers"`: `17`
- `"counts"."content_items"`: `27`
- `"all_validators_pass"`: `true`

No entries yet in `data/victor_instructions.md` since the 2026-08-17 ones
already ACKED (governance-layer scope decision, DeepSeek pre-approval
pending `DEEPSEEK_API_KEY` secret). Nothing new to action from that file
this run.

Status: heartbeat automation is live and healthy (4/4 validators passing,
kill switch off). Still blocked on the open item from 2026-08-17: which AI
powers product-discovery/content automation is decided (DeepSeek,
pre-approved) but `DEEPSEEK_API_KEY` has not been added as a GitHub secret
on this repo yet — cannot start that build until it exists. No other
decision needed from me this run.

## 2026-08-18 — Correction + content-review results + new discovery script

**Correction to my previous entry above**: `DEEPSEEK_API_KEY` was already
added as a GitHub secret before this entry — I was wrong to report it as
missing. Confirmed live: `scripts/content_review.py` + the daily
`content-review` job in `.github/workflows/rio.yml` (commit `84dae99`) had
already run successfully against `data/status.json.content_review` and
`data/content_review_report.json` before I checked.

**Content-review results (DeepSeek reading RIO's own live articles as a
skeptical Indian shopper)**: 21/23 articles reviewed this run (2 hit
network timeouts, not content problems — will retry next scheduled run).
Average score 4.4/10. Only 10/21 articles scored "would_trust". Recurring
gaps flagged across multiple articles: no real price/price range, no exact
dimensions, no honest cons, no delivery/return info. At least one article
(`best-balcony-storage-solutions-india.html`) was flagged as "a placeholder
with no actual product verdict... just a framework and a promise to verify
later" — worth a look since that's the kind of thin/unsubstantiated content
Section 5 asks me to flag rather than let ride.

**New build this run**: `scripts/discover_products.py` + a third daily
workflow job (`discover-products`, ~11:00 IST). This addresses a real gap I
found while looking at the pipeline: 22 published article clusters exist,
but `data/product_candidates.csv` only tracks 8 candidates across 6
clusters — most published topics have zero candidate in the pipeline at
all, i.e. discovery/top-of-funnel has been effectively stalled since the
initial 8 were entered.

What it does, and does not do: DeepSeek suggests Amazon.in search queries
and a short rationale per uncovered cluster; the script writes those as new
`product_candidates.csv` rows with `status=DISCOVERY_REQUIRED` only. It
never writes a merchant, ASIN, price, or canonical URL — those fields stay
blank, exactly as `validate_product_candidates.py` already requires for
that status — and it strips/ignores any such field even if DeepSeek's
response includes one, as a code-level safety net, not just a prompt
instruction. Every row still needs the same human/browser
DISCOVERY_REQUIRED → DISCOVERED → IDENTITY_REVIEW → ... live-verification
work as the existing 8 candidates before it can move further. Capped at 5
new rows/run, idempotent (skips clusters it already covered). Validated
locally against `validate_product_candidates.py` (PASS) before pushing.

No decision needed from me on this build. Flagging for awareness: once it
starts producing DISCOVERY_REQUIRED rows, someone (me on a future
non-scheduled pass, or a human) needs to actually do the live-verification
work to move them forward — the script only ever gets the funnel to the
same starting line the other 8 candidates started from.
