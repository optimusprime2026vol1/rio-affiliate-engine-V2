#!/usr/bin/env python3
import json, os, urllib.request

KEY=(os.environ.get('AWS_BEDROCK_API_KEY') or '').strip()
URL='https://bedrock-mantle.us-east-1.api.aws/v1/chat/completions'
MODEL='qwen.qwen3-coder-next'
OUT='data/Rule book.txt'

prompt=("You are RIO's AWS Bedrock AI engine. Return exactly one plain-text sentence and nothing else: "
        "I'll follow all the rules given by founder and Victor.")
req=urllib.request.Request(URL,data=json.dumps({'model':MODEL,'messages':[{'role':'user','content':prompt}],'temperature':0}).encode(),method='POST',headers={'Content-Type':'application/json','Authorization':f'Bearer {KEY}'})
with urllib.request.urlopen(req,timeout=120) as r: body=json.load(r)
text=((body.get('choices') or [{}])[0].get('message') or {}).get('content') or ''
text=text.strip().strip('`').strip()
expected="I'll follow all the rules given by founder and Victor."
if text != expected:
    raise SystemExit('Bedrock returned unexpected content: '+repr(text[:300]))
with open(OUT,'w',encoding='utf-8') as f:
    f.write(text+'\n')
print(text)
