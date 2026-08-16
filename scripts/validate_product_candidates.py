#!/usr/bin/env python3
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"data"/"product_candidates.csv"
valid={"DISCOVERY_REQUIRED","DISCOVERED","IDENTITY_REVIEW","SPEC_REVIEW","SCORED","OFFER_MAPPING","READY","QUARANTINED","REJECTED"}
errors=[]
with P.open(encoding="utf-8",newline="") as f:
    for r in csv.DictReader(f):
        cid=r["candidate_id"]
        if r["status"] not in valid: errors.append(f"{cid}: invalid status")
        if r["status"]!="DISCOVERY_REQUIRED":
            for k in ("merchant","merchant_product_id","product_title","canonical_url","observed_at"):
                if not r[k].strip(): errors.append(f"{cid}: {r['status']} but {k} missing")
        if r["status"]=="READY":
            try: score=float(r["commercial_score"])
            except: score=-1
            if score < 70: errors.append(f"{cid}: READY below score threshold")
            if r["identity_confidence"]!="VERIFIED_LIVE": errors.append(f"{cid}: READY without VERIFIED_LIVE identity")
            if r["availability_observed"]!="LIVE_VERIFIED_IN_STOCK": errors.append(f"{cid}: READY without LIVE_VERIFIED_IN_STOCK status")
if errors:
    print("PRODUCT INTELLIGENCE GATE: FAIL")
    print("\\n".join(errors)); sys.exit(1)
print("PRODUCT INTELLIGENCE GATE: PASS")
