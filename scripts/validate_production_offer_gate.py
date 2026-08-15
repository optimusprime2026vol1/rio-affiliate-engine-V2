#!/usr/bin/env python3
import csv,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P=R/"data"/"product_candidates.csv"
errors=[]
ready=0
with P.open(encoding="utf-8",newline="") as f:
    for r in csv.DictReader(f):
        if r["status"]=="READY":
            ready+=1
            if r["identity_confidence"]!="VERIFIED_LIVE": errors.append(f"{r['candidate_id']}: READY without VERIFIED_LIVE")
print(f"PRODUCTION OFFER GATE: {'FAIL' if errors else 'PASS'}; READY={ready}")
for e in errors: print(e)
sys.exit(1 if errors else 0)
