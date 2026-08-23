#!/usr/bin/env python3
import json, os, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

KEY=(os.environ.get('ANTHROPIC_API_KEY') or '').strip()
MODEL=os.environ.get('ANTHROPIC_MODEL_RIO','claude-sonnet-4-20250514')
OUT='data/claude_direct_test_result.json'
IST=timezone(timedelta(hours=5,minutes=30))
result={'tested_at':datetime.now(IST).isoformat(timespec='seconds'),'model':MODEL,'ok':False}
if not KEY:
    result['error']='ANTHROPIC_API_KEY missing in runner'
else:
    payload={'model':MODEL,'max_tokens':300,'temperature':0,'system':'You are being tested as the primary reasoning engine for RIO. Reply concisely and exactly as requested.','messages':[{'role':'user','content':'Return valid JSON only: {"status":"PASS","engine":"claude","capability":"reasoning+structured-output","note":"direct API test successful"}'}]}
    req=urllib.request.Request('https://api.anthropic.com/v1/messages',data=json.dumps(payload).encode(),method='POST',headers={'content-type':'application/json','x-api-key':KEY,'anthropic-version':'2023-06-01'})
    try:
        with urllib.request.urlopen(req,timeout=90) as r: body=json.load(r)
        text=''.join((p.get('text') or '') for p in body.get('content',[]) if p.get('type')=='text').strip(); result['http_status']=200; result['response']=text[:1000]
        try:
            parsed=json.loads(text); result['parsed']=parsed; result['ok']=parsed.get('status')=='PASS' and parsed.get('engine')=='claude'
        except Exception as e: result['error']='response was not valid JSON: '+str(e)
    except urllib.error.HTTPError as e:
        result['http_status']=e.code; result['error']=e.read().decode(errors='replace')[:1200]
    except Exception as e: result['error']=str(e)
with open(OUT,'w',encoding='utf-8') as f: json.dump(result,f,indent=2,ensure_ascii=False); f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k!='response'},ensure_ascii=False))
raise SystemExit(0 if result.get('ok') else 1)
