# RIO 3.0 — Core Definition

**Version locked**: 2026-08-23  
**Status**: Initial foundation. Objective and workflow locked. Strategy can be refined later without breaking this core.

---

## 1. What RIO 3.0 Is

RIO is an India-focused affiliate content and authority engine.

**Primary positioning (RIO 3.0)**:

> Help Indian interior designers, contractors, and small offices use AI tools and practical digital products to design faster, present better, and manage projects more efficiently.

**Supporting layer** (already live):
- Compact-home storage, kitchen/bathroom/wardrobe/balcony organisers, and baby-proofing/home-safety products for Indian rented homes.

This creates two coherent content lines under one brand:
1. **Expert / Professional line** — AI tools, design software, productivity, office setup, project tools (higher commission potential).
2. **Home & Living line** — verified physical products already live on the site (Amazon Associates).

Both lines share the same non-negotiable discipline:  
**Discovery → Live-verify → Score → Publish**. Nothing goes live without real verification.

---

## 2. Updated Objective (Locked)

**Primary target**: ₹10,00,000 net approved affiliate commission per month, as soon as realistically possible.

**Reality frame** (do not drop this):
- This is a 12–24 month target under sustained execution, not weeks.
- Track **approved** revenue only (never booked/gross).
- Diversification guardrails by month 12:
  - No single traffic source > 50%
  - No single merchant > 30% of approved revenue
  - At least 3 monetisation mechanisms live
  - At least 25% repeat traffic from owned channels (email / Telegram / WhatsApp)

**Long-term ceiling**: ₹50 lakh+/month remains the aspirational scale target once the authority + multi-channel system is proven.

---

## 3. Audience Priority (Locked for Phase 1)

| Priority | Audience | Why |
|----------|----------|-----|
| 1 | Indian interior designers, contractors, fit-out professionals | Matches Founder's real domain expertise |
| 2 | Small offices / home-office professionals in India | Natural overlap with tools + furniture |
| 3 | Renters / compact-home owners seeking practical storage & safety | Existing proven content base |

Do not try to serve "everyone". Content must stay coherent.

---

## 4. Initial Workflow (RIO 3.0 — Phase 1)

This is the starting operating loop. It can be expanded later.

### Daily / Automated (already exists)
1. Heartbeat every 30 min → validators + dashboard
2. Daily content review (DeepSeek)
3. Daily product discovery suggestions (DISCOVERY_REQUIRED only)
4. Instagram publish attempt (currently blocked on token)

### Weekly Operating Rhythm (new for 3.0)
1. **Review content scores** from `content_review_report.json`
2. **Prioritise 2–3 thin articles** for improvement (add real prices, dimensions, honest cons, comparisons)
3. **Discover / verify** 1–2 new high-intent products or tools that fit the professional audience
4. **Publish or update** only after X-to-X + live verification pass
5. **Report** clearly in `data/rio_report_to_victor.md`

### Content Types to Produce (in order of priority)
1. **Proof-based tutorials** — "How I used X tool to create a mood board / estimate / presentation"
2. **Honest comparisons** — Tool A vs Tool B for Indian designers
3. **Buying guides** with real measurements, prices, and limitations (existing home products + new office tools)
4. **Short-form video scripts** ready for Instagram Reels / YouTube Shorts (faceless or voice — Founder decision pending)

### What is deliberately NOT in the initial workflow
- Mass AI-generated thin articles
- Promoting products without live verification
- Attaching Founder's real name/credentials to public content without explicit sign-off
- Creating new accounts or handling credentials
- Paid ads without explicit budget approval

---

## 5. Monetisation Layers (Priority Order)

1. **Amazon Associates India** (`rioaffiliate-21`) — already live, keep running
2. **Higher-ticket AI / SaaS / design tools** (Impact, PartnerStack, Adobe, Canva, etc.) — once Founder completes account setup
3. **EarnKaro / Cuelinks** — second merchant network (account already exists)
4. **Display ads (AdSense)** — waiting on Google approval
5. **Telegram / WhatsApp deal drops** — after channel identity is created by Founder

---

## 6. Non-Negotiables (Carried Forward Unchanged)

- No fabricated prices, ratings, reviews, ASINs, or "verified" claims.
- Every offer must pass live verification + X-to-X integrity gate before going live.
- Revenue stays ₹0 on public site and dashboard until real approved commissions exist.
- No Founder name, photo, or professional claim goes public without explicit review and approval.
- No account creation, credential handling, or payment actions by the operating agent.
- Do not soften evidence standards to hit targets faster.

---

## 7. Runtime AI Provider Policy

This section defines the current operating provider hierarchy. It does not change the locked business objective or evidence rules.

- **Primary runtime AI:** AWS Bedrock `qwen.qwen3-coder-next` (reported as `bedrock-qwen`).
- **Fallback 1:** DeepSeek `deepseek-chat`.
- **Fallback 2 / emergency:** AWS Bedrock `zai.glm-4.7-flash` (reported as `bedrock-glm`).
- References to DeepSeek elsewhere in this document, such as daily content review, describe a task-specific model and **do not mean DeepSeek is the primary runtime AI**.
- When Founder asks which AI is active, RIO must report the **actual engine used for that request** from runtime metadata. Runtime execution metadata overrides static documentation for this question.
- Provider changes must never weaken RIO rules, validators, evidence standards, or Founder controls.

---

## 8. Version Control Note

- This file (`data/RIO_3.0_DEFINITION.md`) is the source of truth for the 3.0 objective and initial workflow.
- Strategy details, content calendar, and specific tool lists can be updated in separate files later without rewriting this core.
- When major changes are made, append a dated note at the bottom of this file.

---

**Created**: 2026-08-23 by RIO operating agent on Founder direction to move to Version 3.0.

**Updated 2026-08-23**: Added explicit runtime AI provider hierarchy after Bedrock Qwen webhook execution became active. Business objective and evidence rules unchanged.
