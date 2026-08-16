# RIO Telegram "Deal Drop" Content Format

Drafted 2026-08-16 by Dr. Victor, per BUSINESS_STRATEGY.md "Immediate next
actions" item 4 and Vicky's confirmed decision to launch a Telegram deals
channel. This is a content template only -- posting is not automated yet, and
nothing publishes until Vicky creates the Telegram channel (channel creation
is founder-only, see the setup checklist).

## Why this format, not a copy of the article pages

Telegram deal channels succeed on speed and scannability, not long-form
copy -- readers scroll fast and decide in seconds. Every "deal drop" pulls
directly from RIO's already-verified `offer_identity_registry.csv` rows, so
it inherits the same no-fabrication rule as the website: only offers with
`publish_status=READY` and a `price_checked_at` from that day (or the day
of the post) may go out, and prices are always described as "at last check,"
never asserted as a live real-time price on Telegram itself, since Telegram
posts (unlike the website) cannot auto-refresh their text.

## Post template

```
🏠 [Product name, short form]
[One-line practical benefit -- what problem it solves, not generic praise]

💰 ₹[price] (checked [date]) — verify current price before buying, Amazon
prices change often
⭐ [rating] · [review count] ratings
🔗 [tagged Amazon link]

[One-line disclosure, every single post, never omitted:]
Affiliate link — RIO may earn a commission. Price shown was last checked on
[date]; confirm on Amazon before buying.
```

## Worked example (using a live, already-READY offer)

```
🏠 EUDELE No-Drill Bathroom Shelf (Pack of 2)
For rented bathrooms — no drilling, holds up well per 42,000+ ratings.

💰 ₹643 (checked 16 Aug) — verify current price before buying, Amazon
prices change often
⭐ 4.4 · 42,330 ratings
🔗 https://www.amazon.in/dp/B0GYYRR5JB?tag=rioaffiliate-21

Affiliate link — RIO may earn a commission. Price shown was last checked on
16 Aug 2026; confirm on Amazon before buying.
```

## Rules (non-negotiable, same spirit as the website's X→X policy)

1. Only post offers with `publish_status=READY` in `offer_identity_registry.csv`.
2. Price/rating/review-count in the post must match the most recent
   `price_checked_at` value for that offer -- never estimate or round up a
   rating, never invent a review count.
3. Every post includes the disclosure line, not just a pinned channel-level
   disclosure -- Telegram deal channels are covered by the same ASCI
   influencer-disclosure expectations as the website.
4. If an offer's price changes materially before a scheduled post goes out,
   re-check it live first (same rule as the website's
   price-sensitive-creative-refreshed-at-publish-time policy) -- do not post
   stale prices just because the post was drafted in advance.
5. Cadence: start at 3-4 posts/week (matches current READY offer count of
   10 without repeating the same product too often), not daily -- quality
   and accuracy over volume, especially while the channel is new and trust
   is being built.
6. No fake urgency ("only 2 left!", countdown timers) unless that claim is
   actually visible and verified on the Amazon listing itself at post time.

## What's still needed before this can go live

- Vicky creates the Telegram channel (channel name, description, @handle) --
  founder-only per Section 6 (RIO does not create accounts).
- Once the channel exists, RIO can draft a rotating posting queue from the
  10 current READY offers and hand it to Vicky (or a scheduled task) to
  post manually at first; full automation (bot posting) is a later step,
  not needed to start.
