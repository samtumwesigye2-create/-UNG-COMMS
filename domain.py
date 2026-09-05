from dataclasses import dataclass, asdict
from uuid import uuid4
@dataclass
class Message:
    id:str; channel:str; recipient:str; body:str; status:str="queued"
_messages={}
def queue_message(channel:str, recipient:str, body:str):
    m=Message(str(uuid4()),channel,recipient,body); _messages[m.id]=m; return asdict(m)
def list_messages(): return [asdict(x) for x in _messages.values()]
