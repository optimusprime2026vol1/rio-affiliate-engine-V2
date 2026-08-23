#!/usr/bin/env python3
import json, os, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

KEY=(os.environ.get('AWS_BEDROCK_API_KEY') or '').strip()
MODEL=os.environ.get('AWS_BEDROCK_MODEL_RIO','openai.gpt-5.6-terra').strip() or 'openai.gpt-5.6-terra'
REGION=os.environ.get('AWS_BEDROCK_REGION','us-east-1').strip() or 'us-east-1'
BASE=f'https://bedrock-mantle.{REGION}.api.aws/v1'
OUT='data/bedrock_terra_direct_test_result.json'
IST=timezone(timedelta(hours=5,minutes=30))
result={'tested_at':datetime.now(IST).isoformat(timespec='seconds'),'model':MODEL,'region':REGION,'endpoint':BASE,'ok':False}

if not KEY:
    result['error']='AWS_BEDROCK_API_KEY missing in runner'
else:
    payload={
      'model':MODEL,
      'messages':[{'role':'user','content':'Reply exactly with valid JSON only: {"status":"PASS","engine":"bedrock-terra","note":"direct API test successful"}'}],
      'temperature':0
    }
    req=urllib.request.Request(
      BASE+'/chat/completions',
      data=json.dumps(payload).encode(),
      method='POST',
      headers={'Content-Type':'application/json','Authorization':f'Bearer {KEY}'}
    )
    try:
        with urllib.request.urlopen(req,timeout=120) as r:
            body=json.load(r)
        result['http_status']=200
        content=((body.get('choices') or [{}])[0].get('message') or {}).get('content') or ''
        result['response']=content[:1200]
        try:
            parsed=json.loads(content)
            result['parsed']=parsed
            result['ok']=parsed.get('status')=='PASS' and parsed.get('engine')=='bedrock-terra'
        except Exception as e:
            result['error']='response was not valid expected JSON: '+str(e)
    except urllib.error.HTTPError as e:
        result['http_status']=e.code
        result['error']=e.read().decode(errors='replace')[:1500]
    except Exception as e:
        result['error']=str(e)

with open(OUT,'w',encoding='utf-8') as f:
    json.dump(result,f,indent=2,ensure_ascii=False); f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k!='response'},ensure_ascii=False))
raise SystemExit(0 if result.get('ok') else 1)
