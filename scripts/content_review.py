#!/usr/bin/env python3
"""RIO — Content Conversion Review: DeepSeek reviews RIO's own LIVE, already-
published articles (not candidate products — see the scope note below) as a
skeptical Indian online shopper, and flags what's hurting trust/conversion.

Scope, deliberately narrow: this script reviews existing content quality. It
does NOT discover new products, does NOT invent prices/ASINs/availability,
and does NOT touch data/product_candidates.csv or
data/offer_identity_registry.csv. Per RIO_OPERATING_AGENT_BRIEF.md Section 5
("No fabricated prices, ratings, reviews, 'verified' claims, or ASINs...
every promoted product requires a real, live check") an LLM chat API cannot
safely do product discovery or live-verification on its own — that stays a
human/browser-verified process. What DeepSeek CAN safely do is critique
writing/structure/trust-signals on content that's already live, exactly the
same "independent reviewer" role business_review.py plays for AURA.

Reads the live site's own sitemap.xml (checked out locally under site/) so
this always reviews what's ACTUALLY published, not a stale CSV status field
(data/content_queue.csv's status column was found to be unreliable/stale
against the real deployed site — see data/victor_instructions.md 2026-08-17).

Writes: data/content_review_report.json (per-article verdicts) and folds a
short summary into data/status.json under "content_review" (merges, does not
overwrite the fields scripts/heartbeat.py owns).
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import deepseek_client

ROOT = os.path.join(os.path.dirname(__file__), "..")
SITE = os.path.join(ROOT, "site")
MAX_CHARS = 4000  # keep prompts a sane size; article body text, not the whole HTML doc

PERSONA_PROMPT_TMPL = """You are a price-conscious Indian online shopper reading a product buying-guide
article before deciding whether to click through and buy. You have been burned before by fake
reviews and generic "best products" listicles with no real substance. You are actively comparing
this article against other sources open in your other tabs.

Read this article's text content (from a real, live page) and answer ONLY with compact JSON, no
markdown fences: {{"would_trust": true/false, "would_click_buy_link": true/false,
"missing_trust_signals": ["<short phrase>", ...], "biggest_weakness": "<one short sentence>",
"score": <integer 0-10>}}

Rules:
- would_trust must be false if the article reads like generic AI filler, has no real
  measurements/specifics, or makes claims that sound unverifiable.
- missing_trust_signals: things a skeptical Indian buyer looks for that are ABSENT here — e.g.
  real price mentioned, exact dimensions, material specifics, who it's/isn't good for, honest
  cons, delivery/return info, disclosure of affiliate relationship (note: disclosure IS required
  content on this site — if you don't see it in this excerpt, don't assume it's missing sitewide,
  just don't count that as a signal to require in the excerpt).
- score: 0 = would bounce immediately, 10 = fully convinced, would click through and buy.

ARTICLE TEXT (may be truncated):
---
{text}
---
"""


def strip_html(html):
    html = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style\b[^>]*>.*?</style>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_sitemap_article_paths():
    sm_path = os.path.join(SITE, "sitemap.xml")
    try:
        xml = open(sm_path, encoding="utf-8").read()
    except Exception as e:
        print(f"[content_review] could not read {sm_path}: {e}")
        return []
    locs = re.findall(r"<loc>(.*?)</loc>", xml)
    paths = []
    for loc in locs:
        # sitemap entries look like "./articles/xyz.html" or an absolute URL ending the same way
        m = re.search(r"(articles/[\w\-./]+\.html)$", loc.strip())
        if m:
            paths.append(m.group(1))
    return sorted(set(paths))


def jload(p, default):
    try:
        return json.load(open(os.path.join(ROOT, p)))
    except Exception:
        return default


def jsave(p, obj):
    path = os.path.join(ROOT, p)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path, "w"), indent=1, ensure_ascii=False)


def main():
    if not deepseek_client.available():
        print("[content_review] DEEPSEEK_API_KEY not set — nothing to do, skipping (fail open).")
        return

    article_paths = load_sitemap_article_paths()
    print(f"[content_review] {len(article_paths)} live articles found in site/sitemap.xml")

    report = jload("data/content_review_report.json", {})
    reviewed = 0
    errors = 0
    for rel_path in article_paths:
        full_path = os.path.join(SITE, rel_path)
        if not os.path.exists(full_path):
            print(f"[content_review] SKIP (sitemap references missing file): {rel_path}")
            continue
        try:
            html = open(full_path, encoding="utf-8").read()
            text = strip_html(html)[:MAX_CHARS]
            if len(text) < 200:
                print(f"[content_review] SKIP (too little text extracted, {len(text)} chars): {rel_path}")
                continue
            verdict = deepseek_client.ask_json(PERSONA_PROMPT_TMPL.format(text=text))
            report[rel_path] = {
                "would_trust": bool(verdict.get("would_trust")),
                "would_click_buy_link": bool(verdict.get("would_click_buy_link")),
                "missing_trust_signals": verdict.get("missing_trust_signals", []),
                "biggest_weakness": verdict.get("biggest_weakness", ""),
                "score": verdict.get("score"),
            }
            reviewed += 1
            print(f"[content_review] {rel_path}: score={verdict.get('score')} "
                  f"trust={verdict.get('would_trust')} weakness={verdict.get('biggest_weakness')!r}")
        except Exception as e:
            report[rel_path] = {"error": str(e)}
            errors += 1
            print(f"[content_review] ERROR reviewing {rel_path}: {e}")

    jsave("data/content_review_report.json", report)

    scored = [v["score"] for v in report.values() if isinstance(v, dict) and isinstance(v.get("score"), (int, float))]
    avg_score = round(sum(scored) / len(scored), 1) if scored else None
    would_trust_count = sum(1 for v in report.values() if isinstance(v, dict) and v.get("would_trust"))

    status = jload("data/status.json", {})
    status["content_review"] = {
        "reviewed_this_run": reviewed,
        "errors_this_run": errors,
        "total_articles_in_report": len(report),
        "avg_score": avg_score,
        "would_trust_count": would_trust_count,
    }
    jsave("data/status.json", status)
    print(f"[content_review] done: reviewed={reviewed} errors={errors} avg_score={avg_score}")


if __name__ == "__main__":
    main()
