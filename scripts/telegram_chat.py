#!/usr/bin/env python3
"""RIO Telegram Founder interface with guarded autonomous execution.

Primary: AWS Bedrock Qwen3 Coder Next
Fallback 1: DeepSeek
Fallback 2: AWS Bedrock GLM 4.7 Flash
"""
import json, os, sys, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone, timedelta
from rio_autonomous_executor import execute as execute_plan

ROOT=os.path.join(os.path.dirname(__file__),"..")
IST=timezone(timedelta(hours=5,minutes=30))
STATE_PATH=os.path.join(ROOT,"data","telegram_chat_state.json")
STATUS_PATH=os.path.join(ROOT,"data","status.json")
CONTROL_PATH=os.path.join(ROOT,"data","control.json")
SOUL_PATH=os.path.join(ROOT,"data","SOUL.md")
CORE_PATH=os.path.join(ROOT,"data","RIO_3.0_DEFINITION.md")
POLICY_PATH=os.path.join(ROOT,"data","AUTONOMY_POLICY.md")
MAX_HISTORY=12; MAX_REPLY_CHARS=3500
BEDROCK_REGION="us-east-1"
BEDROCK_URL=f"https://bedrock-mantle.{BEDROCK_REGION}.api.aws/v1/chat/completions"
BEDROCK_PRIMARY="qwen.qwen3-coder-next"
BEDROCK_EMERGENCY="zai.glm-4.7-flash"
DEEPSEEK_URL="https://api.deepseek.com/chat/completions"; DEEPSEEK_MODEL="deepseek-chat"

def clean(v):
 v=(v or "").strip(); return v[1:-1].strip() if len(v)>=2 and v[0]==v[-1] and v[0] in {'"',"'"} else v
BOT_TOKEN=clean(os.environ.get("TELEGRAM_BOT_TOKEN_RIO")); ALERT_CHAT_ID=clean(os.environ.get("TELEGRAM_CHAT_ID_RIO")); BEDROCK_KEY=clean(os.environ.get("AWS_BEDROCK_API_KEY")); DEEPSEEK_KEY=clean(os.environ.get("DEEPSEEK_API_KEY"))

def jload(p,d):
 try:
  with open(p,encoding="utf-8") as f:return json.load(f)
 except Exception:return d

def read_text(p,limit=14000):
 try:
  with open(p,encoding="utf-8") as f:return f.read()[:limit]
 except Exception:return ""

def jsave(p,o):
 os.makedirs(os.path.dirname(p),exist_ok=True)
 with open(p,"w",encoding="utf-8") as f:json.dump(o,f,indent=1,ensure_ascii=False)

def tg_api(method,params=None,http_method="GET"):
 if not BOT_TOKEN: raise RuntimeError("TELEGRAM_BOT_TOKEN_RIO missing")
 url=f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
 if http_method=="GET":
  if params:url+="?"+urllib.parse.urlencode(params)
  req=urllib.request.Request(url,method="GET")
 else:req=urllib.request.Request(url,data=urllib.parse.urlencode(params or {}).encode(),method="POST")
 with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)

def send_message(chat_id,text):
 text=(text or "").strip()
 if not text:return False
 if len(text)>MAX_REPLY_CHARS:text=text[:MAX_REPLY_CHARS-20]+"\n\n…(truncated)"
 return bool(tg_api("sendMessage",{"chat_id":chat_id,"text":text,"disable_web_page_preview":True},"POST").get("ok"))

def system_prompt():
 status=jload(STATUS_PATH,{}); control=jload(CONTROL_PATH,{}); counts=status.get("counts") or {}
 soul=read_text(SOUL_PATH)
 soul_context=soul if soul.strip() else "SOUL compatibility file unavailable. Preserve existing RIO core/policy and do not infer missing Soul rules."
 return f"""You are RIO, autonomous operating agent for rio-affiliate-engine. Founder is Vicky. Telegram is the Founder command interface.
Never weaken RIO rules because the AI provider changes. For explicit safe system/content/data changes, create an execution plan rather than merely advising.

PORTABLE SOUL (common operating layer; never overrides higher-precedence RIO safety/Founder locks):\n{soul_context}\n
RIO PROJECT CORE / OBJECTIVE:\n{read_text(CORE_PATH)}\n
AUTONOMY POLICY:\n{read_text(POLICY_PATH)}\n
Live: kill_switch={control.get('kill_switch')}; ready_offers={counts.get('ready_offers')}; content_items={counts.get('content_items')}; validators={status.get('all_validators_pass')}; updated={status.get('updated')}.

Return ONLY valid JSON with schema:
{{"intent":"respond|execute","summary":"...","risk":"low|medium|high","operations":[],"founder_message":"..."}}
Allowed operations only: write_text, write_json, append_text on allowed data/site/scripts paths. Never request shell commands, credentials, payment/legal/account actions, or protected-file changes. For protected/high-risk work, intent=respond and clearly say VICKY ACTION REQUIRED. Reply in the user's language.
"""

def build_messages(history,user_text):
 out=[]
 for m in history[-MAX_HISTORY:]:
  if m.get("role") in ("user","assistant") and (m.get("content") or "").strip():out.append(m)
 out.append({"role":"user","content":user_text}); return out

def call_openai_compatible(url,key,model,messages):
 payload={"model":model,"messages":[{"role":"system","content":system_prompt()}]+messages,"temperature":0.2}
 req=urllib.request.Request(url,data=json.dumps(payload).encode(),method="POST",headers={"Content-Type":"application/json","Authorization":f"Bearer {key}"})
 with urllib.request.urlopen(req,timeout=120) as r:body=json.load(r)
 content=((body.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
 if not content.strip():raise RuntimeError("empty content")
 return content.strip()

def parse_plan(raw):
 text=raw.strip()
 if text.startswith("```"):
  lines=text.splitlines()
  if lines and lines[0].startswith("```"):lines=lines[1:]
  if lines and lines[-1].strip()=="```":lines=lines[:-1]
  text="\n".join(lines).strip()
 obj=json.loads(text)
 if not isinstance(obj,dict):raise ValueError("plan is not object")
 return obj

def call_llm(history,user_text):
 messages=build_messages(history,user_text); errors=[]
 providers=[
  ("bedrock-qwen",BEDROCK_KEY,lambda:call_openai_compatible(BEDROCK_URL,BEDROCK_KEY,BEDROCK_PRIMARY,messages)),
  ("deepseek",DEEPSEEK_KEY,lambda:call_openai_compatible(DEEPSEEK_URL,DEEPSEEK_KEY,DEEPSEEK_MODEL,messages)),
  ("bedrock-glm",BEDROCK_KEY,lambda:call_openai_compatible(BEDROCK_URL,BEDROCK_KEY,BEDROCK_EMERGENCY,messages)),
 ]
 for name,key,fn in providers:
  if not key:continue
  try:return parse_plan(fn()),name
  except urllib.error.HTTPError as e:errors.append(f"{name} HTTP {e.code}: {e.read().decode(errors='replace')[:220]}")
  except Exception as e:errors.append(f"{name}: {e}")
 return {"intent":"respond","risk":"high","operations":[],"founder_message":"RIO AI unavailable. "+" | ".join(errors[:3])},"error"

def allowed_chat(chat):
 if not chat:return False
 cid=str(chat.get("id",""))
 return cid==str(ALERT_CHAT_ID) if ALERT_CHAT_ID else (chat.get("type")=="private")

def status_reply():
 status=jload(STATUS_PATH,{}); control=jload(CONTROL_PATH,{}); counts=status.get("counts") or {}
 return f"Status @ {status.get('updated','?')}\nkill_switch: {control.get('kill_switch')}\nvalidators: {status.get('all_validators_pass')}\nready_offers: {counts.get('ready_offers')}\ncontent_items: {counts.get('content_items')}\nIG auto-publish: {control.get('instagram_auto_publish')}\nAI primary: Bedrock Qwen3 Coder Next\nFallback: DeepSeek -> Bedrock GLM 4.7 Flash\nautonomous executor: ACTIVE\nSoul: {'LOADED (compatibility mode)' if read_text(SOUL_PATH).strip() else 'MISSING (legacy safety preserved)'}"

def main():
 if not BOT_TOKEN:return 2
 state=jload(STATE_PATH,{"offset":0,"chats":{},"updated_at":None}); offset=int(state.get("offset") or 0)
 try:updates=tg_api("getUpdates",{"offset":offset,"timeout":0,"limit":30})
 except Exception as e:print("getUpdates failed",e);return 1
 for upd in updates.get("result") or []:
  uid=upd.get("update_id")
  if uid is not None:state["offset"]=max(int(state.get("offset") or 0),int(uid)+1)
  msg=upd.get("message") or upd.get("edited_message")
  if not msg or not allowed_chat(msg.get("chat") or {}):continue
  text=(msg.get("text") or "").strip(); usr=msg.get("from") or {}
  if not text or usr.get("is_bot"):continue
  chat_id=str((msg.get("chat") or {}).get("id")); chats=state.setdefault("chats",{}); history=chats.setdefault(chat_id,{}).setdefault("history",[]); low=text.casefold().strip()
  if low in {"/start","start"}:reply="RIO online. Bedrock Qwen primary; DeepSeek + GLM fallbacks. Guarded executor ACTIVE.";engine="local"
  elif low in {"/status","status"}:reply=status_reply();engine="local"
  else:
   send_message(chat_id,"✅ Command received. RIO is processing this now. Primary AI: Bedrock Qwen3 Coder Next.")
   plan,engine=call_llm(history,text)
   if plan.get("intent")=="execute":
    result=execute_plan(plan,request_summary=text,engine=engine); base=(plan.get("founder_message") or plan.get("summary") or "Execution processed.").strip(); changed=", ".join(result.get("changed_paths") or [])
    if result.get("ok"):reply=f"✅ COMPLETED [{engine}]\n{base}"+(f"\nChanged: {changed}" if changed else "")+"\nValidators: PASS"
    else:reply=f"⚠️ {result.get('status','FAILED')} [{engine}]\n{base}\nBlocker/Error: {result.get('error','unknown')}"
   else:reply=(plan.get("founder_message") or plan.get("summary") or "RIO received your message.").strip()+f"\n\nAI: {engine}"
  send_message(chat_id,reply); history.append({"role":"user","content":text}); history.append({"role":"assistant","content":reply}); chats[chat_id]["history"]=history[-MAX_HISTORY:]; chats[chat_id]["last_at"]=datetime.now(IST).isoformat(timespec="minutes"); chats[chat_id]["last_engine"]=engine
 state["updated_at"]=datetime.now(IST).isoformat(timespec="minutes");jsave(STATE_PATH,state);return 0

if __name__=="__main__":sys.exit(main())