import sys
from pathlib import Path
import pandas as pd,plotly.express as px,streamlit as st
sys.path.insert(0,str(Path(__file__).parent/'src'))
from studypilot.documents import parse
from studypilot.retrieval import Retriever
from studypilot.ai import answer,summarise,make_quiz
from studypilot.db import register,login,log,history
st.set_page_config(page_title='StudyPilot AI Ultimate',page_icon='🧠',layout='wide');st.markdown(Path('style.css').read_text(),unsafe_allow_html=True)
for k,v in {'user':None,'chunks':[],'retriever':None,'modules':{},'summary':'','quiz':''}.items():st.session_state.setdefault(k,v)
with st.sidebar:
 st.title('🧠 StudyPilot AI')
 api=st.text_input('Gemini API key (optional)',type='password',help='Enables high-quality grounded answers, summaries and quizzes. It is not saved by the app.')
 if not st.session_state.user:
  mode=st.radio('Account',['Login','Register'],horizontal=True);u=st.text_input('Username');p=st.text_input('Password',type='password')
  if st.button(mode,use_container_width=True):
   ok=login(u,p) if mode=='Login' else register(u,p)
   if ok:st.session_state.user=u;st.rerun()
   else:st.error('Invalid details. Password requires 8+ characters.')
 else:
  st.success(f'Welcome, {st.session_state.user}')
  if st.button('Log out'):st.session_state.user=None;st.rerun()
if not st.session_state.user:
 st.markdown('<div class="hero"><span class="pill">Grounded RAG</span><span class="pill">Learning Analytics</span><h1>Learn deeply from your own notes.</h1><p>Accurate, cited and modern academic support.</p></div>',unsafe_allow_html=True);st.stop()
st.markdown('<div class="hero"><span class="pill">BM25 + FAISS</span><span class="pill">Gemini grounded synthesis</span><h1>StudyPilot AI Ultimate</h1><p>Upload, understand, revise, practise and track progress.</p></div>',unsafe_allow_html=True)
tabs=st.tabs(['📚 Modules','✨ Ask Tutor','📝 Revision Notes','🧠 Quiz','📄 Past Paper','✅ Assignment Check','📊 Progress','🗓 Planner'])
with tabs[0]:
 module=st.text_input('Module name',placeholder='Software Development');files=st.file_uploader('Upload text-based PDF notes',type='pdf',accept_multiple_files=True)
 if st.button('Build module knowledge base') and module and files:
  with st.spinner('Cleaning, chunking and indexing...'):
   cs=parse([(f.name,f.getvalue()) for f in files],module);st.session_state.modules[module]=cs;st.session_state.chunks=cs;st.session_state.retriever=Retriever(cs)
  st.success(f'{len(cs)} traceable sections indexed for {module}.')
 if st.session_state.modules:
  choice=st.selectbox('Active module',list(st.session_state.modules))
  if st.button('Switch module'):
   st.session_state.chunks=st.session_state.modules[choice];st.session_state.retriever=Retriever(st.session_state.chunks);st.rerun()
with tabs[1]:
 q=st.text_input('Ask a focused question')
 if q and st.session_state.retriever:
  hits=st.session_state.retriever.search(q);ans,cites=answer(q,hits,api);log(st.session_state.user,'question',1)
  st.markdown(f'<div class="answer">{ans}</div>',unsafe_allow_html=True)
  if cites:st.caption('Evidence: '+' • '.join(f'{s}, page {p}' for s,p in cites))
  with st.expander('Inspect retrieved evidence'):
   for h in hits:st.markdown(f'<div class="card"><b>{h.chunk.source}, page {h.chunk.page}</b> · score {h.score:.2f}<br>{h.chunk.text}</div>',unsafe_allow_html=True)
with tabs[2]:
 if st.button('Generate structured revision notes'):
  st.session_state.summary=summarise(st.session_state.chunks,api);log(st.session_state.user,'summary',1)
 if st.session_state.summary:st.markdown(st.session_state.summary)
with tabs[3]:
 if st.button('Generate 5 evidence-based MCQs'):st.session_state.quiz=make_quiz(st.session_state.chunks,api);log(st.session_state.user,'quiz',1)
 if st.session_state.quiz:st.markdown(st.session_state.quiz)
with tabs[4]:
 pp=st.file_uploader('Upload past paper PDF',type='pdf',key='past')
 if pp and st.button('Analyse past paper'):
  pcs=parse([(pp.name,pp.getvalue())],'Past Paper');st.markdown(summarise(pcs,api))
with tabs[5]:
 brief=st.text_area('Assignment brief');draft=st.text_area('Your draft')
 if st.button('Analyse coverage') and brief and draft:
  prompt=f"""Compare the DRAFT against the BRIEF. Do not write the assignment. Return covered requirements, missing requirements, improvement checklist and word count. BRIEF:{brief} DRAFT:{draft}"""
  from studypilot.ai import call
  try:result=call(prompt,api) or 'Add a Gemini API key for semantic requirement analysis.'
  except Exception:result='Analysis failed. Check the API key.'
  st.markdown(result);st.metric('Draft words',len(draft.split()))
with tabs[6]:
 rows=history(st.session_state.user)
 if rows:
  df=pd.DataFrame(rows,columns=['Activity','Value','Date']);counts=df.groupby('Activity').size().reset_index(name='Count');st.plotly_chart(px.bar(counts,x='Activity',y='Count',color='Activity',template='plotly_dark'),use_container_width=True)
 else:st.info('Use the learning tools to build analytics.')
with tabs[7]:
 exam=st.date_input('Exam date');hours=st.slider('Hours per day',1,8,2);topics=st.text_area('Topics, one per line')
 if st.button('Create active-recall study plan') and topics:
  df=pd.DataFrame([{'Day':i+1,'Topic':t.strip(),'Learn':f'{hours*35} min','Recall':f'{hours*15} min','Practice':f'{hours*10} min'} for i,t in enumerate(topics.splitlines()) if t.strip()]);st.dataframe(df,use_container_width=True);st.download_button('Download plan',df.to_csv(index=False),'study_plan.csv')
st.caption('Use cited pages to verify learning. AI output can be wrong. Do not upload confidential material or use generated text as your own assessed work.')
