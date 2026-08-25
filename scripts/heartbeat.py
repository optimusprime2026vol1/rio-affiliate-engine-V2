#!/usr/bin/env python3
"""RIO heartbeat: self-monitoring runtime health loop.

Runs without Founder action on schedule, refreshes dashboard/status, runs safety
validators, observes SOUL runtime integrity, and sends Telegram only on material
health-state transitions. SOUL remains observe-only in this migration stage.
"""
import json, os, subprocess, sys, urllib.request, urllib.parse
from datetime import datetime, timezone, timedelta

ROOT=os.path.join(os.path.dirname(__file__),"..")
IST=timezone(timedelta(hours=5,minutes=30))
REPO=os.environ.get("GITHUB_REPOSITORY","vickykenin-lang/rio-affiliate-engine")
TOK=os.environ.get("GITHUB_TOKEN","")
BOT=(os.environ.get("TELEGRAM_BOT_TOKEN_RIO") or "").strip()
CHAT=(os.environ.get("TELEGRAM_CHAT_ID_RIO") or "").strip()
OWNER="vickykenin-lang"
ALERT_STATE="data/heartbeat_alert_state.json"

def gh(path,data=None,method=None):
 req=urllib.request.Request(f"https://api.github.com/{path}",method=method,headers={"Authorization":f"Bearer {TOK}","Accept":"application/vnd.github+json","Content-Type":"application/json"})
 body=json.dumps(data).encode() if data is not None else None
 with urllib.request.urlopen(req,body,timeout=30) as r:return json.load(r) if r.status!=204 else {}

def jload(p,d):
 try:
  with open(os.path.join(ROOT,p),encoding="utf-8") as f:return json.load(f)
 except Exception:return d

def jsave(p,o):
 path=os.path.join(ROOT,p);os.makedirs(os.path.dirname(path),exist_ok=True)
 with open(path,"w",encoding="utf-8") as f:json.dump(o,f,indent=1,ensure_ascii=False)

def notify(text):
 if not BOT or not CHAT:
  print("[heartbeat] Telegram secrets missing; alert not sent");return False
 data=urllib.parse.urlencode({"chat_id":CHAT,"text":text,"disable_web_page_preview":True}).encode()
 req=urllib.request.Request(f"https://api.telegram.org/bot{BOT}/sendMessage",data=data,method="POST")
 try:
  with urllib.request.urlopen(req,timeout=20) as r:body=json.load(r)
  return bool(body.get("ok"))
 except Exception as e:
  print("[heartbeat] Telegram alert failed:",e);return False

def run_script(name):
 try:
  r=subprocess.run([sys.executable,os.path.join(ROOT,"scripts",name)],cwd=ROOT,capture_output=True,text=True,timeout=120)
  out=(r.stdout or "")+(("\n"+r.stderr) if r.stderr else "")
  return r.returncode==0,out.strip()
 except Exception as e:return False,f"failed to run {name}: {e}"

control=jload("data/control.json",{"kill_switch":False,"kill_reason":None})
inbox=jload("data/inbox.json",{"messages":[]})
now=datetime.now(IST).isoformat(timespec="minutes")
try:issues=gh(f"repos/{REPO}/issues?state=open&per_page=50")
except Exception as e:print("[heartbeat] issue read failed:",e);issues=[]
for i in issues:
 labels=[l["name"] for l in i.get("labels",[])];title=(i.get("title") or "").upper();body=i.get("body") or ""
 try:
  if "kill-switch" in labels or "KILL SWITCH" in title:
   control["kill_switch"]=True;control["kill_reason"]=f"Issue #{i['number']} by {i['user']['login']} at {now}";gh(f"repos/{REPO}/issues/{i['number']}",{"state":"closed"},"PATCH")
  elif title.startswith("RESUME") and i["user"]["login"]==OWNER:
   control["kill_switch"]=False;control["kill_reason"]=None;gh(f"repos/{REPO}/issues/{i['number']}",{"state":"closed"},"PATCH")
  elif "owner-message" in labels or "MESSAGE TO RIO" in title:
   inbox["messages"].append({"at":now,"from":i["user"]["login"],"issue":i["number"],"text":body[:2000]});gh(f"repos/{REPO}/issues/{i['number']}",{"state":"closed"},"PATCH")
 except Exception as e:print("[heartbeat] issue handling failed:",e)
jsave("data/control.json",control);jsave("data/inbox.json",inbox)
if control.get("kill_switch"):
 status=jload("data/status.json",{});status.update({"updated":now,"kill_switch":True,"note_en":f"Paused by kill switch. {control.get('kill_reason','')}"});jsave("data/status.json",status);sys.exit(0)

production_ok,production_out=run_script("check_production.py")
dash_ok,dash_out=run_script("generate_dashboard.py")
validator_scripts={"production_live":None,"offer_integrity":"validate_offer_integrity.py","product_candidates":"validate_product_candidates.py","dashboard":"validate_dashboard.py","production_offer_gate":"validate_production_offer_gate.py"}
validators={}
for key,script in validator_scripts.items():
 ok,out=(production_ok,production_out) if script is None else run_script(script)
 validators[key]={"pass":ok,"detail":"\n".join(out.splitlines()[-15:])};print(f"[heartbeat] {key}: {'PASS' if ok else 'FAIL'}")
all_pass=all(v["pass"] for v in validators.values()) and dash_ok
snap=jload("data/dashboard_snapshot.json",{})
counts={k:snap.get(k,0) for k in ["product_candidates","ready_offers","blocked_offers","rejected_products","content_items","revenue_inr","cost_inr","net_profit_inr"]};counts["production_verified"]=bool(production_ok)
status=jload("data/status.json",{});status.update({"updated":now,"kill_switch":False,"dashboard_regenerated":dash_ok,"validators":validators,"all_validators_pass":all_pass,"counts":counts,"heartbeat_interval_minutes":5,"runtime_primary_ai":"bedrock-qwen","runtime_fallbacks":["deepseek","bedrock-glm"]})
status["note_en"]=(f"Heartbeat OK — {sum(1 for v in validators.values() if v['pass'])}/{len(validators)} validators passing." if all_pass else f"⚠ Heartbeat failure — {sum(1 for v in validators.values() if not v['pass'])} validator(s) failing. Publishing/deployment must remain blocked until recovery.")
jsave("data/status.json",status)

# Compatibility-stage SOUL observation. It runs after status is refreshed so it can
# verify the live AI/validator binding. Its result is recorded but does NOT affect
# all_validators_pass, kill switch, publishing gates, or autonomous execution yet.
soul_ok,soul_out=run_script("soul_runtime.py")
soul_state=jload("data/soul_runtime_status.json",{})
status=jload("data/status.json",{})
status["soul_runtime"]={
 "mode":soul_state.get("mode","compatibility_observe"),
 "valid":bool(soul_state.get("valid")) if soul_state else bool(soul_ok),
 "hard_fail_closed":False,
 "soul_sha256":soul_state.get("soul_sha256"),
 "execution_effect":"NONE",
}
jsave("data/status.json",status)
print(f"[heartbeat] soul_runtime: {'PASS' if soul_ok else 'OBSERVE_FAIL'}")
if soul_out:print("[heartbeat] soul detail:","\n".join(soul_out.splitlines()[-5:]))

prev=jload(ALERT_STATE,{"healthy":None});was=prev.get("healthy")
if was is not None and was!=all_pass:
 if all_pass:notify("🟢 RIO RECOVERED\nHeartbeat and validators are healthy again. Autonomous operation can continue under normal gates.")
 else:
  failed=[k for k,v in validators.items() if not v["pass"]]
  notify("🔴 RIO ISSUE DETECTED\nHeartbeat/validator failure: "+", ".join(failed)+"\nRIO has not weakened publish gates. Technical review required if it does not self-recover.")
jsave(ALERT_STATE,{"healthy":all_pass,"updated":now,"soul_valid":status.get("soul_runtime",{}).get("valid")})
print("heartbeat done",json.dumps({"ok":all_pass,"soul_observed":status.get("soul_runtime",{}).get("valid"),"counts":counts}))
