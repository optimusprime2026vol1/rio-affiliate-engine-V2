#!/usr/bin/env python3
import csv, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/"data"/"offer_identity_registry.csv"
required_identity=("product_name","merchant","merchant_product_id","variant","canonical_url",
                   "creative_product_name","creative_variant","expected_landing_product","expected_landing_variant")
errors=[]
with REG.open(encoding="utf-8", newline="") as f:
    for r in csv.DictReader(f):
        oid=r["offer_id"]
        if r["publish_status"]=="READY":
            for k in required_identity:
                if not r[k].strip(): errors.append(f"{oid}: READY but {k} is blank")
            if r["identity_status"]!="VERIFIED": errors.append(f"{oid}: READY but identity_status != VERIFIED")
            if r["availability_status"]!="IN_STOCK": errors.append(f"{oid}: READY but availability_status != IN_STOCK")
            if r["affiliate_status"]!="ACTIVE": errors.append(f"{oid}: READY but affiliate_status != ACTIVE")
            pairs=[
                ("product",r["creative_product_name"],r["expected_landing_product"]),
                ("variant",r["creative_variant"],r["expected_landing_variant"]),
            ]
            for label,a,b in pairs:
                if a.strip().casefold()!=b.strip().casefold():
                    errors.append(f"{oid}: X→X {label} mismatch")
        elif r["publish_status"] not in ("BLOCKED","PAUSED"):
            errors.append(f"{oid}: invalid publish_status {r['publish_status']}")
if errors:
    print("X→X GATE: FAIL")
    print("\\n".join(errors))
    sys.exit(1)
print("X→X GATE: PASS")
