#!/usr/bin/env python3
"""Run one safe objective-driven RIO business cycle from persistent work memory."""
import json, os, re, sys, urllib.parse, urllib.request
from pathlib import Path
from telegram_chat import call_llm
from rio_autonomous_executor import execute as execute_plan
from rio_work_dashboard import record

ROOT=Path(__file__).resolve().parents[1]; WORK=ROOT/'data/rio_work_status.json'; SNAPSHOT=ROOT/'data/dashboard_snapshot.json'; STATUS=ROOT/'data/status.json'; CONTROL=ROOT/'data/control.json'; AUDIT=ROOT/'data/autonomy_audit.jsonl'
BOT=(os.environ.get('TELEGRAM_BOT_TOKEN_RIO') or '').strip(); CHAT=(os.environ.get('TELEGRAM_CHAT_ID_RIO') or '').strip()
PILLARS={1:'website development/conversion/SEO',2:'new affiliate networks and product opportunities',3:'AdSense readiness and monetization',4:'product-led blog/content',5:'Flipkart or other commerce/platform expansion',6:'Instagram sales/content execution'}

def jload(p,d):
    try:return json.loads(p.read_text(encoding='utf-8'))
    except Exception:return d

def tail_audit(n=6):
    try:return [json.loads(x) for x in AUDIT.read_text(encoding='utf-8').splitlines()[-n:] if x.strip()]
    except Exception:return []

def notify(text):
    if not BOT or not CHAT:return False
    data=urllib.parse.urlencode({'chat_id':CHAT,'text':text,'disable_web_page_preview':True}).encode(); req=urllib.request.Request(f'https://api.telegram.org/bot{BOT}/sendMessage',data=data,method='POST')
    try:
        with urllib.request.urlopen(req,timeout=20) as r:return bool(json.load(r).get('ok'))
    except Exception:return False

def completed(memory,limit=18):
    out=[]
    for x in reversed(memory.get('history') or []):
        if x.get('status')=='COMPLETED':
            t=' '.join(str(x.get('task') or '').lower().split())
            if t and t not in out:out.append(t)
            if len(out)>=limit:break
    return out

def pillar_for(text):
    t=(text or '').lower()
    if any(x in t for x in ['instagram','carousel','reel','social post']):return 6
    if any(x in t for x in ['flipkart','commerce platform','marketplace','merchant platform']):return 5
    if any(x in t for x in ['blog','guide','article','content']):return 4
    if any(x in t for x in ['adsense','ad monet','display ad']):return 3
    if any(x in t for x in ['affiliate network','affiliate program','new network','partner program']):return 2
    if any(x in t for x in ['website','site/','seo','index','comparison page','landing page','conversion']):return 1
    return None

def recent_pillars(memory,n=8):return [pillar_for(x.get('task')) for x in (memory.get('history') or []) if x.get('status')=='COMPLETED'][-n:]

def main():
    control=jload(CONTROL,{'kill_switch':False}); memory=jload(WORK,{}); snap=jload(SNAPSHOT,{}); health=jload(STATUS,{})
    if control.get('kill_switch') or health.get('all_validators_pass') is not True:return 0
    if memory.get('status')=='WORKING':return 0
    if memory.get('founder_action_needed') or memory.get('status') in {'BLOCKED','VICKY_ACTION_REQUIRED'}:return 0
    done=completed(memory); rp=recent_pillars(memory); counts={p:rp.count(p) for p in PILLARS}; lastp=rp[-1] if rp else None
    # Diversity algorithm: no more than 2 consecutive completions in one pillar; favor least-used pillars in recent window.
    forced_rotate=len(rp)>=2 and rp[-1] is not None and rp[-1]==rp[-2]
    eligible=[p for p in PILLARS if not(forced_rotate and p==lastp)]
    min_count=min(counts[p] for p in eligible); priority=[p for p in eligible if counts[p]==min_count]
    context={'status':memory.get('status','IDLE'),'last_completed':memory.get('last_completed'),'last_result':memory.get('last_result'),'next_task':memory.get('next_task'),'changed_files':memory.get('changed_files') or [],'recent_completed_task_keys':done,'recent_pillars':rp,'pillar_counts_recent':counts,'rotation_priority_pillars':priority,'forced_rotate_away_from':lastp if forced_rotate else None,'recent_history':(memory.get('history') or [])[-14:],'recent_audit':tail_audit(),'business_snapshot':{k:snap.get(k,0) for k in ['ready_offers','blocked_offers','content_items','revenue_inr','net_profit_inr','instagram_posted']}}
    rules=("AUTONOMOUS PHASE-2 PORTFOLIO CYCLE. Continue persistent memory and choose EXACTLY ONE safe repository task. Six locked pillars are: "+json.dumps(PILLARS)+". Apply this scheduling algorithm: (1) external-event next_task is WAITING, never repeat work to fill time; (2) never repeat/substantially clone recent completed deliverables; (3) maximum TWO consecutive completed tasks in the same pillar; after two, MUST rotate to another pillar; (4) prefer rotation_priority_pillars, especially pillars with zero/lowest recent work, unless there is a documented urgent revenue/safety reason; (5) maximum TWO deliverables for the same product/campaign before switching product/campaign or pillar until new external evidence arrives; (6) prioritize work by expected revenue impact x readiness x evidence, then reduce blockers; (7) maintain useful parallel progress across all six pillars rather than exhausting one pillar; (8) account signup, credentials, payment, legal/compliance acceptance, publishing to external accounts, or unverifiable external metrics require waiting/Founder action as appropriate. If preferred work waits on external data, pivot to another independent pillar. If no safe independent repository task exists, respond WAITING_EXTERNAL:. founder_message must state PILLAR:<1-6>, task, why, changes, and NEXT_TASK:. Memory:\n"+json.dumps(context,ensure_ascii=False))
    record('WORKING',current_task=memory.get('next_task') or 'Selecting diversified Phase-2 task.',engine='selecting',validators='PRECHECK_PASS',founder_action_needed=False)
    plan,engine=call_llm([],rules); summary=(plan.get('founder_message') or plan.get('summary') or '').strip()
    if plan.get('intent')!='execute':
        if summary.upper().startswith('WAITING_EXTERNAL:'):
            record('WAITING',current_task=memory.get('next_task') or 'Waiting for external evidence',engine=engine,validators='NOT_RUN',result=summary,next_task=memory.get('next_task'),blocker=None,founder_action_needed=False); return 0
        record('VICKY_ACTION_REQUIRED',current_task=memory.get('next_task') or 'Autonomous continuation',engine=engine,validators='NOT_RUN',result=summary or 'No executable safe task.',blocker=summary,founder_action_needed=True); notify('⚠️ RIO FOUNDER ACTION REQUIRED\n'+summary[:3000]); return 0
    chosen=(plan.get('summary') or memory.get('next_task') or 'Autonomous Phase-2 task').strip(); ck=' '.join(chosen.lower().split()); cp=pillar_for(summary+' '+chosen)
    if ck in done or (forced_rotate and cp==lastp):
        record('WAITING',current_task=chosen,engine=engine,validators='NOT_RUN',result='PORTFOLIO_GUARD: repeated task/pillar concentration suppressed; next cycle must rotate.',next_task='Choose an independent task from a least-used eligible Phase-2 pillar.',blocker=None,founder_action_needed=False); return 0
    record('WORKING',current_task=chosen,engine=engine,validators='RUNNING',founder_action_needed=False); result=execute_plan(plan,request_summary='AUTONOMOUS PHASE-2: '+chosen,engine=engine); changed=result.get('changed_paths') or []
    if result.get('ok'):
        nxt=None; low=summary.lower(); marker='next_task:'
        if marker in low:nxt=summary[low.rfind(marker)+len(marker):].strip().splitlines()[0][:500] or None
        nxt=nxt or 'Choose the next highest-impact safe task using six-pillar rotation, evidence, and anti-repeat rules.'
        record('COMPLETED',current_task=chosen,engine=engine,changed_files=changed,validators='PASS',result=summary or 'Autonomous task completed and validated.',next_task=nxt,blocker=None,founder_action_needed=False); return 0
    status=result.get('status','FAILED'); error=result.get('error','unknown'); fn=status=='VICKY_ACTION_REQUIRED'; record(status,current_task=chosen,engine=engine,changed_files=[],validators='FAIL',result=summary,next_task=memory.get('next_task'),blocker=error,founder_action_needed=fn)
    if fn:notify(f'⚠️ RIO FOUNDER ACTION REQUIRED\nTask: {chosen}\nBlocker: {error}'[:3500])
    return 0

if __name__=='__main__':sys.exit(main())
