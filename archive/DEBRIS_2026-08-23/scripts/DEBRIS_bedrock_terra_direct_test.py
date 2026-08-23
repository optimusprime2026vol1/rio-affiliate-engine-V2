#!/usr/bin/env python3
import json, os, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta
KEY=(os.environ.get('AWS_BEDROCK_API_KEY') or '').strip(); REGION='us-east-1'; BASE=f'https://bedrock-mantle.{REGION}.api.aws/v1'; OUT='data/bedrock_terra_direct_test_result.json'; IST=timezone(timedelta(hours=5,minutes=30))
CANDIDATES=['xai.grok-4.3','zai.glm-4.7-flash','qwen.qwen3-coder-next']
result={'tested_at':datetime.now(IST).isoformat(timespec='seconds'),'region':REGION,'endpoint':BASE,'ok':False,'attempts':[]}
if not KEY: result['error']='AWS_BEDROCK_API_KEY missing in runner'
else:
 for model in CANDIDATES:
  a={'model':model,'ok':False}; payload={'model':model,'messages':[{'role':'user','content':'Reply exactly with valid JSON only: {"status":"PASS","engine":"bedrock"}'}],'temperature':0}
  req=urllib.request.Request(BASE+'/chat/completions',data=json.dumps(payload).encode(),method='POST',headers={'Content-Type':'application/json','Authorization':f'Bearer {KEY}'})
  try:
   with urllib.request.urlopen(req,timeout=120) as r: body=json.load(r)
   a['http_status']=200; content=((body.get('choices') or [{}])[0].get('message') or {}).get('content') or ''; a['response']=content[:800]
   try: a['parsed']=json.loads(content); a['ok']=a['parsed'].get('status')=='PASS'
   except Exception as e: a['error']='invalid expected JSON: '+str(e)
  except urllib.error.HTTPError as e: a['http_status']=e.code; a['error']=e.read().decode(errors='replace')[:1200]
  except Exception as e: a['error']=str(e)
  result['attempts'].append(a)
  if a['ok']: result['ok']=True; result['working_model']=model; break
with open(OUT,'w',encoding='utf-8') as f: json.dump(result,f,indent=2,ensure_ascii=False); f.write('\n')
print(json.dumps({'ok':result['ok'],'working_model':result.get('working_model'),'attempt_count':len(result['attempts'])}))
raise SystemExit(0 if result['ok'] else 1)
