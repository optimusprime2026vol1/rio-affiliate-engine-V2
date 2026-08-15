import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'data/unit_economics.json'
d=json.loads(p.read_text())
a=d['assumptions']; o=d['outputs']
clicks=round(a['monthly_sessions']*a['affiliate_click_through_rate'])
orders=round(clicks*a['merchant_conversion_rate'])
commission=orders*a['average_order_value_inr']*a['commission_rate']
assert clicks==o['affiliate_clicks']
assert orders==o['orders']
assert commission==o['gross_affiliate_commission_inr']
print('PASS: unit economics arithmetic consistent')
