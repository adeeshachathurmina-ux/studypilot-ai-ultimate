import re,faiss,numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from .models import Hit
def tok(x):return re.findall(r'\w+',x.casefold(),re.UNICODE)
def scale(a):
 a=np.asarray(a,'float32');lo,hi=a.min(),a.max()
 return np.zeros_like(a) if hi==lo else (a-lo)/(hi-lo)
class Retriever:
 def __init__(self,chunks):
  if not chunks:raise ValueError('No readable PDF text found.')
  self.c=chunks;self.b=BM25Okapi([tok(x.text) for x in chunks]);self.m=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
  e=self.m.encode([x.text for x in chunks],normalize_embeddings=True,show_progress_bar=False).astype('float32');self.i=faiss.IndexFlatIP(e.shape[1]);self.i.add(e)
 def search(self,q,k=5):
  lex=np.asarray(self.b.get_scores(tok(q)),'float32');qe=self.m.encode([q],normalize_embeddings=True,show_progress_bar=False).astype('float32');d,ix=self.i.search(qe,len(self.c));sem=np.zeros(len(self.c),'float32')
  for j,s in zip(ix[0],d[0],strict=True):sem[j]=s
  score=.65*scale(sem)+.35*scale(lex);order=np.argsort(score)[::-1][:k]
  return [Hit(self.c[j],float(score[j])) for j in order]
