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
