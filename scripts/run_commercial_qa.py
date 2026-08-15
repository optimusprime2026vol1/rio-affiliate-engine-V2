#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=["validate_offer_integrity.py","validate_product_candidates.py"]
failed=False
for c in checks:
    p=subprocess.run([sys.executable,str(ROOT/"scripts"/c)],text=True,capture_output=True)
    print(f"== {c} =="); print(p.stdout.strip())
    if p.returncode: failed=True
sys.exit(1 if failed else 0)
