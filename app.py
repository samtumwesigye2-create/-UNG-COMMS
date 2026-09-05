from fastapi import FastAPI,Header,HTTPException
from pydantic import BaseModel
from domain import queue_message,list_messages
from integration import dependencies
SYSTEM_ID="UNG-HERMES"; LEGACY_ID="UNG-COMMS"; VERSION="0.2.0"
app=FastAPI(title=SYSTEM_ID,version=VERSION,description="UNG Communications System")
class MessageIn(BaseModel): channel:str; recipient:str; body:str
def auth(p,h):
 s={x.strip() for x in (h or "").split(",") if x.strip()}
 if p not in s and "ung.admin" not in s: raise HTTPException(403,"UNG-JANUS permission required")
@app.get("/")
def root(): return {"system":SYSTEM_ID,"legacy_id":LEGACY_ID,"status":"online","version":VERSION}
@app.get("/health")
def health(): return {"status":"ok","service":SYSTEM_ID,"version":VERSION}
@app.get("/ready")
def ready(): return {"status":"ready","service":SYSTEM_ID,"dependencies":dependencies()}
@app.get("/v1/system")
def system(): return {"system_id":SYSTEM_ID,"legacy_id":LEGACY_ID,"domain":"communications","dependencies":dependencies()}
@app.get("/v1/messages")
def messages(x_ung_permissions:str|None=Header(None)): auth("hermes.messages.read",x_ung_permissions); return list_messages()
@app.post("/v1/messages",status_code=202)
def send(body:MessageIn,x_ung_permissions:str|None=Header(None)): auth("hermes.messages.send",x_ung_permissions); return queue_message(body.channel,body.recipient,body.body)
