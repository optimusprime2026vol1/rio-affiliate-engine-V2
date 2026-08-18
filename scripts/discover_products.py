#!/usr/bin/env python3
"""RIO — Product Discovery Suggestions: DeepSeek proposes WHAT to go look for
next (search queries + rationale), for content clusters that have zero
product_candidates.csv rows today. It does not, and per
RIO_OPERATING_AGENT_BRIEF.md Section 5 must not, invent a specific ASIN,
price, canonical URL, or availability claim — those all require a real live
check by a human or a browser tool, never an LLM chat response.

Every row this script writes has status=DISCOVERY_REQUIRED, which
validate_product_candidates.py explicitly exempts from needing
merchant/merchant_product_id/canonical_url/observed_at — those columns are
left blank on purpose. The next step in the pipeline (DISCOVERY_REQUIRED ->
DISCOVERED -> IDENTITY_REVIEW -> ...) is unchanged human/browser work, same
as every existing candidate in this file was produced.

Safety net beyond the prompt wording: even if DeepSeek's JSON response
includes an asin/price/url field (models sometimes do this despite
instructions), this script never reads or writes those fields — only
`search_queries` (text) and `rationale` (text) are used, both go straight
into review_notes as clearly-labeled unverified suggestions.

Idempotent + capped: only clusters with zero existing candidate_id rows are
considered, and at most MAX_NEW_PER_RUN rows are appended per run, so this
can run unattended on a schedule without runaway growth.
"""
import csv, os, re, sys
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(__file__))
import deepseek_client

ROOT = os.path.join(os.path.dirname(__file__), "..")
CSV_PATH = os.path.join(ROOT, "data", "product_candidates.csv") if os.path.exists(
    os.path.join(ROOT, "data", "product_candidates.csv")) else os.path.join(ROOT, "product_candidates.csv")
ARTICLES_DIR = os.path.join(ROOT, "site", "articles")
IST = timezone(timedelta(hours=5, minutes=30))
MAX_NEW_PER_RUN = 5

FIELDS = ["candidate_id", "cluster", "merchant", "merchant_product_id", "product_title",
          "brand", "model", "variant", "canonical_url", "price_observed", "currency",
          "availability_observed", "spec_source", "observed_at", "identity_confidence",
          "commercial_score", "status", "review_notes"]

PROMPT_TMPL = """You are helping a home & living affiliate content researcher decide WHAT product
to go look for next on Amazon.in for the buying-guide topic "{topic}" (article slug: {slug}).

You must NOT name a specific ASIN, exact price, or claim any product is currently in stock —
you have no way to verify that right now, and doing so would be a fabricated claim. Only suggest
what to search for and why.

Answer ONLY with compact JSON, no markdown fences:
{{"search_queries": ["2-3 realistic amazon.in search phrases a researcher should type"],
 "rationale": "1-2 sentences on what kind of product/spec/price-band fits this topic and why",
 "cluster_slug": "a short kebab-case product-cluster id, e.g. under-sink-organizer"}}"""


def slug_to_topic(slug):
    return slug.replace("-india", "").replace("-", " ").strip()


def load_candidates():
    if not os.path.exists(CSV_PATH):
        return [], FIELDS
    with open(CSV_PATH, encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        rows = list(r)
        fields = r.fieldnames or FIELDS
    return rows, fields


def existing_clusters(rows):
    return {r["cluster"].strip().lower() for r in rows if r.get("cluster", "").strip()}


def article_slugs():
    if not os.path.isdir(ARTICLES_DIR):
        return []
    return sorted(f[:-5] for f in os.listdir(ARTICLES_DIR) if f.endswith(".html"))


def next_candidate_id(rows):
    nums = []
    for r in rows:
        m = re.match(r"CAND_[A-Z]+_(\d+)$", r.get("candidate_id", ""))
        if m:
            nums.append(int(m.group(1)))
    n = (max(nums) + 1) if nums else 1
    return f"CAND_DISC_{n:03d}"


def main():
    if not deepseek_client.available():
        print("[discover] DEEPSEEK_API_KEY not set — nothing to do.")
        return 0

    rows, fields = load_candidates()
    covered = existing_clusters(rows)
    slugs = article_slugs()

    # A slug "covers" a cluster if the cluster string appears in the slug or
    # vice versa (loose match — clusters are hand-picked short ids, slugs are
    # full article names) so we don't re-suggest topics already in the funnel.
    uncovered = [s for s in slugs if not any(c in s or s in c for c in covered)]

    if not uncovered:
        print("[discover] every article slug already has a matching candidate cluster — nothing to do.")
        return 0

    now = datetime.now(IST).strftime("%Y-%m-%d")
    new_rows = []
    errors = []
    for slug in uncovered[:MAX_NEW_PER_RUN]:
        topic = slug_to_topic(slug)
        try:
            data = deepseek_client.ask_json(PROMPT_TMPL.format(topic=topic, slug=slug))
        except Exception as e:
            errors.append(f"{slug}: {e}")
            continue
        queries = data.get("search_queries") or []
        rationale = str(data.get("rationale") or "").strip()
        cluster = str(data.get("cluster_slug") or slug).strip().lower()
        cluster = re.sub(r"[^a-z0-9-]+", "-", cluster).strip("-") or slug
        if cluster in covered:
            continue  # DeepSeek proposed a cluster id we already have — skip, not a fabrication risk, just a dupe
        cid = next_candidate_id(rows + new_rows)
        row = {k: "" for k in fields}
        row.update({
            "candidate_id": cid,
            "cluster": cluster,
            "observed_at": now,
            "status": "DISCOVERY_REQUIRED",
            "review_notes": (
                f"DeepSeek discovery suggestion {now} for article slug '{slug}' — UNVERIFIED, no "
                f"ASIN/price/URL/availability has been checked yet, requires the normal "
                f"DISCOVERY_REQUIRED->DISCOVERED live-verification steps before this can move "
                f"further. Suggested Amazon.in search queries: {'; '.join(queries) or '(none given)'}. "
                f"Rationale: {rationale or '(none given)'}"
            ),
        })
        new_rows.append(row)
        covered.add(cluster)

    if new_rows:
        with open(CSV_PATH, "a", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            for row in new_rows:
                w.writerow(row)
        print(f"[discover] appended {len(new_rows)} DISCOVERY_REQUIRED row(s): "
              f"{', '.join(r['candidate_id'] for r in new_rows)}")
    else:
        print("[discover] no new rows written this run.")

    if errors:
        print("[discover] errors:\n" + "\n".join(errors))

    return 0


if __name__ == "__main__":
    sys.exit(main())
