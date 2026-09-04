# StudyPilot AI Ultimate

A modern, grounded academic learning platform for university students.

## Complete features
- Secure local login with PBKDF2 password hashing
- Module-based PDF knowledge bases
- Clean PDF extraction and page-preserving chunks
- Hybrid BM25 + FAISS retrieval
- Optional Gemini 3.8 Flash grounded synthesis
- Direct answers with evidence inspection and page citations
- Structured revision notes
- Evidence-based MCQ generation
- Past-paper analysis
- Assignment brief versus draft analysis
- Learning activity dashboard
- Active-recall study planner and CSV export
- Animated futuristic UI

## Accuracy design
The app retrieves evidence before generating answers. Gemini is instructed to use only retrieved context and cite pages. Without an API key, a conservative extractive fallback is used. AI output is never guaranteed correct, so cited pages remain visible for verification.

## Run on Windows
```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Gemini setup
Get a Gemini API key from Google AI Studio. Enter it in the app sidebar. The app does not persist the key. Alternatively copy `.env.example` to `.env` and add the key locally. Never commit `.env`.

## Tests
```powershell
python -m pytest
```

## Limitations
Text-based PDFs work best. Scanned PDFs need OCR. Accuracy depends on source-note quality, extraction quality, retrieval and model behaviour. Do not claim 100% accuracy.
