import os,re
from google import genai
MODEL='gemini-3.8-flash'
def context(hits):return '\n\n'.join(f'[SOURCE {i}: {h.chunk.source}, page {h.chunk.page}]\n{h.chunk.text}' for i,h in enumerate(hits,1))
def call(prompt,key=''):
 api=key.strip() or os.getenv('GEMINI_API_KEY','').strip()
 if not api:return None
 with genai.Client(api_key=api) as client:
  r=client.interactions.create(model=MODEL,input=prompt)
  return r.output_text.strip()
def answer(question,hits,key=''):
 if not hits or hits[0].score<.18:return 'I could not find enough evidence in the uploaded notes.',[]
 cites=sorted({(h.chunk.source,h.chunk.page) for h in hits[:3]})
 prompt=f"""You are an academic tutor. Answer ONLY from CONTEXT. If context is insufficient, say exactly: Not enough information in the uploaded notes.
Give: (1) a direct definition, (2) a clear explanation, (3) concise bullet points if useful. Do not invent facts. Add citations like [filename, page X] after claims.
QUESTION: {question}
CONTEXT:
{context(hits)}"""
 try:r=call(prompt,key)
 except Exception as e:r=None
 if r:return r,cites
 # safe offline fallback
 text=' '.join(h.chunk.text for h in hits[:2]);parts=[s.strip() for s in re.split(r'(?<=[.!?])\s+',text) if 6<=len(s.split())<=45 and not s.endswith('?')]
 return (' '.join(parts[:3]) or 'Relevant evidence was found, but a clean answer could not be created. Inspect the cited pages.'),cites
def summarise(chunks,key=''):
 ctx='\n\n'.join(f'[{c.source}, page {c.page}] {c.text}' for c in chunks[:35])
 prompt=f"""Create accurate revision notes ONLY from the context. Organise by topic. Include key definitions, explanations, examples and source citations. Exclude slide instructions, questions, repeated headers and noise.
CONTEXT:
{ctx}"""
 try:r=call(prompt,key)
 except Exception:r=None
 if r:return r
 return '\n'.join(f'- {c.text[:220]} [{c.source}, page {c.page}]' for c in chunks[:8])
def make_quiz(chunks,key=''):
 ctx='\n'.join(f'[{c.source}, page {c.page}] {c.text}' for c in chunks[:20])
 prompt=f"""Create 5 high-quality MCQs from the context only. Format each as Q, A-D, Answer, Explanation, Source. Avoid ambiguous questions.
{ctx}"""
 try:return call(prompt,key) or 'AI quiz generation needs a Gemini API key.'
 except Exception:return 'Quiz generation failed. Check the API key and connection.'
