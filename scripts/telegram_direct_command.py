#!/usr/bin/env python3
"""Process one Telegram Founder command supplied by webhook/GitHub workflow."""
import json, os, sys, urllib.request
from telegram_chat import call_llm, send_message
from rio_autonomous_executor import execute as execute_plan

CHAT_ID=(os.environ.get('RIO_COMMAND_CHAT_ID') or '').strip()
COMMAND=(os.environ.get('RIO_COMMAND_TEXT') or '').strip()
COMMAND_ID=(os.environ.get('RIO_COMMAND_ID') or '').strip()
CALLBACK_URL=(os.environ.get('RIO_CALLBACK_URL') or '').strip()
CALLBACK_TOKEN=(os.environ.get('RIO_CALLBACK_TOKEN') or '').strip()


def callback(status, engine='unknown', detail=''):
    if not CALLBACK_URL: return
    payload=json.dumps({'command_id':COMMAND_ID,'status':status,'engine':engine,'detail':detail[:1000]}).encode()
    headers={'Content-Type':'application/json'}
    if CALLBACK_TOKEN: headers['x-rio-callback-token']=CALLBACK_TOKEN
    try:
        req=urllib.request.Request(CALLBACK_URL,data=payload,method='POST',headers=headers)
        urllib.request.urlopen(req,timeout=30).read()
    except Exception as e:
        print('[direct_command] callback failed:',e)


def main():
    if not CHAT_ID or not COMMAND:
        print('[direct_command] missing chat or command')
        return 2
    plan,engine=call_llm([],COMMAND)
    try:
        if plan.get('intent')=='execute':
            result=execute_plan(plan,request_summary=COMMAND,engine=engine)
            base=(plan.get('founder_message') or plan.get('summary') or 'Execution processed.').strip()
            changed=', '.join(result.get('changed_paths') or [])
            if result.get('ok'):
                reply=f"✅ COMPLETED [{engine}]\n{base}"+(f"\nChanged: {changed}" if changed else '')+'\nValidators: PASS'
                status='COMPLETED'
            else:
                reply=f"⚠️ {result.get('status','FAILED')} [{engine}]\n{base}\nBlocker/Error: {result.get('error','unknown')}"
                status=result.get('status','FAILED')
        else:
            reply=(plan.get('founder_message') or plan.get('summary') or 'RIO received your message.').strip()+f"\n\nAI: {engine}"
            status='COMPLETED'
        sent=send_message(CHAT_ID,reply)
        callback(status,engine,reply if not sent else '')
        return 0 if sent else 1
    except Exception as e:
        msg=f"⚠️ FAILED [{engine}]\nRIO could not complete the command. Error: {str(e)[:800]}"
        try: send_message(CHAT_ID,msg)
        except Exception: pass
        callback('FAILED',engine,str(e))
        return 1

if __name__=='__main__': sys.exit(main())
