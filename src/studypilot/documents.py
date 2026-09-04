import hashlib,re
from pathlib import Path
import fitz
from .models import Chunk
NOISE=[r'^page\s*\d+$',r'^\d+$',r'^session\s+\d+',r'^chapter\s+\d+\s*$']
def clean(t):
 t=t.replace('•','\n• ').replace('▪','\n• ').replace('–',' - ')
 lines=[]
 for x in t.splitlines():
  x=re.sub(r'\s+',' ',x).strip()
  if x and not any(re.match(p,x,re.I) for p in NOISE):lines.append(x)
 return '\n'.join(lines)
def units(t):return [x.strip(' •') for x in re.split(r'\n+|(?<=[.!?])\s+',t) if len(x.split())>=3]
def chunks(text,size=110,overlap=15):
 u=units(text);out=[];cur=[]
 for x in u:
  if cur and len(' '.join(cur+[x]).split())>size:
   out.append(' '.join(cur));cur=[' '.join(' '.join(cur).split()[-overlap:]),x]
  else:cur.append(x)
 if cur:out.append(' '.join(cur))
 return out
def parse(files,module):
 out=[]
 for name,data in files:
  safe=Path(name).name
  with fitz.open(stream=data,filetype='pdf') as doc:
   for page,p in enumerate(doc,1):
    text=clean(p.get_text('text'))
    for i,part in enumerate(chunks(text)):
     key=hashlib.sha1(f'{safe}{page}{i}{part}'.encode()).hexdigest()[:12];out.append(Chunk(key,part,safe,page,module))
 return out
