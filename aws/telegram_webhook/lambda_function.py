import json, os, time, urllib.request
import boto3

TABLE=os.environ['COMMAND_TABLE']; BOT_TOKEN=os.environ['TELEGRAM_BOT_TOKEN_RIO']; CHAT_ID=str(os.environ['TELEGRAM_CHAT_ID_RIO']); GH_TOKEN=os.environ['GITHUB_DISPATCH_TOKEN']; GH_REPO=os.environ.get('GITHUB_REPO','vickykenin-lang/rio-affiliate-engine'); CALLBACK_TOKEN=os.environ['RIO_CALLBACK_TOKEN']
ddb=boto3.resource('dynamodb').Table(TABLE); scheduler=boto3.client('scheduler')

def tg_send(chat_id,text):
 data=json.dumps({'chat_id':chat_id,'text':text,'disable_web_page_preview':True}).encode(); req=urllib.request.Request(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',data=data,method='POST',headers={'Content-Type':'application/json'}); urllib.request.urlopen(req,timeout=10).read()

def dispatch(command_id,chat_id,text,callback_url):
 body=json.dumps({'ref':'main','inputs':{'job':'telegram-direct','command_id':command_id,'chat_id':str(chat_id),'command_text':text,'callback_url':callback_url}}).encode(); req=urllib.request.Request(f'https://api.github.com/repos/{GH_REPO}/actions/workflows/rio.yml/dispatches',data=body,method='POST',headers={'Authorization':f'Bearer {GH_TOKEN}','Accept':'application/vnd.github+json','Content-Type':'application/json','User-Agent':'RIO-Webhook'}); urllib.request.urlopen(req,timeout=15).read()

def handler(event,context):
 path=(event.get('rawPath') or '')
 if path.endswith('/callback'):
  hdr={k.lower():v for k,v in (event.get('headers') or {}).items()}
  if hdr.get('x-rio-callback-token')!=CALLBACK_TOKEN:return {'statusCode':403,'body':'forbidden'}
  body=json.loads(event.get('body') or '{}'); cid=body.get('command_id')
  if cid: ddb.update_item(Key={'command_id':cid},UpdateExpression='SET #s=:s, completed_at=:t',ExpressionAttributeNames={'#s':'status'},ExpressionAttributeValues={':s':body.get('status','COMPLETED'),':t':int(time.time())})
  return {'statusCode':200,'body':'ok'}
 if path.endswith('/watchdog'):
  body=json.loads(event.get('body') or '{}'); cid=body.get('command_id'); item=ddb.get_item(Key={'command_id':cid}).get('Item') or {}
  if item.get('status')=='PENDING':
   tg_send(item['chat_id'],'⚠️ RIO TIMEOUT\nCommand 5 minutes mein complete nahi hua. Task ko failed/pending maana gaya hai; technical blocker investigate karna hoga.')
   ddb.update_item(Key={'command_id':cid},UpdateExpression='SET #s=:s',ExpressionAttributeNames={'#s':'status'},ExpressionAttributeValues={':s':'TIMEOUT'})
  return {'statusCode':200,'body':'ok'}
 update=json.loads(event.get('body') or '{}'); msg=update.get('message') or update.get('edited_message') or {}; chat=msg.get('chat') or {}; text=(msg.get('text') or '').strip(); cid=str(chat.get('id',''))
 if not text or cid!=CHAT_ID:return {'statusCode':200,'body':'ignored'}
 command_id=str(update.get('update_id') or int(time.time()*1000)); callback_url=f"https://{event['requestContext']['domainName']}{event['requestContext']['http']['path'].rsplit('/',1)[0]}/callback"
 ddb.put_item(Item={'command_id':command_id,'chat_id':cid,'text':text,'status':'PENDING','created_at':int(time.time()),'ttl':int(time.time())+86400})
 tg_send(cid,'✅ Command received. RIO is processing this now. Primary AI: Bedrock Qwen3 Coder Next.')
 dispatch(command_id,cid,text,callback_url)
 # watchdog scheduling is provisioned by EventBridge Scheduler in deployment; one-shot target calls /watchdog at +5m.
 return {'statusCode':200,'body':'accepted'}
