#!/usr/bin/env python3
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1]
required=[R/'site/dashboard/index.html',R/'data/dashboard_snapshot.json',R/'data/ceo_action_queue.csv']
missing=[str(p) for p in required if not p.exists()]
snap=json.loads((R/'data/dashboard_snapshot.json').read_text()) if not missing else {}
errs=list(missing)
if not isinstance(snap.get('production_verified'), bool): errs.append('production_verified must be a boolean from production health evidence')
if snap.get('revenue_inr')!=0: errs.append('unexpected inferred revenue')
for key in ('instagram_approved','instagram_post_pending','instagram_posted','instagram_failed'):
    if not isinstance(snap.get(key), int): errs.append(f'{key} must be an integer')
if not snap.get('instagram_last_status'): errs.append('instagram_last_status must be visible')
print('CEO DASHBOARD GATE: '+('FAIL' if errs else 'PASS'))
for e in errs: print(e)
sys.exit(1 if errs else 0)
