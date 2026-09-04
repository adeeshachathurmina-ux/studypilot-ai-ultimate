# StudyPilot AI Ultimate 🧠

A modern, source-grounded academic learning platform that helps university students learn directly from their own lecture notes.

StudyPilot AI Ultimate transforms uploaded PDF learning materials into clear explanations, structured revision notes, evidence-based quizzes, past-paper insights, assignment guidance, and personalised study plans. It combines hybrid information retrieval with generative AI while keeping the original source pages visible for verification.

## Live Application

### https://studypilot-ai-ultimate.streamlit.app/

> Create a local demo account, upload a text-based lecture-note PDF, build a module knowledge base, and explore the available learning tools.

---

## The Problem

University students often manage lecture notes, module handbooks, assignments, and past papers across many separate files. Finding a specific explanation inside long PDF documents can be slow and difficult.

General AI assistants may also provide answers that are not supported by the student’s official learning materials.

StudyPilot AI Ultimate addresses these problems by retrieving relevant evidence from uploaded notes before generating an answer. The application also displays the original PDF name and page number so that students can verify the information.

---

## Core Features

### Module-Based Knowledge Bases

- Create separate academic modules
- Upload multiple PDF lecture notes
- Switch between indexed modules
- Keep answers focused on the selected subject

### Source-Grounded AI Tutor

- Ask questions using natural language
- Receive direct definitions and clear explanations
- Generate answers from retrieved lecture-note evidence
- View supporting PDF names and page numbers
- Inspect the original retrieved passages

### Structured Revision Notes

- Generate organised revision materials
- Identify important definitions and concepts
- Exclude repeated slide headers and unnecessary content
- Retain source references for verification

### Evidence-Based Quiz Generation

- Generate multiple-choice questions from lecture notes
- Receive answers and explanations
- Display the original source pages
- Support active recall and self-assessment

### Past-Paper Analysis

- Upload past-paper PDFs
- Analyse assessment content
- Extract important themes and questions
- Support exam preparation using structured insights

### Assignment Requirement Analysis

- Compare an assignment brief with a student draft
- Identify covered requirements
- Highlight potentially missing requirements
- Provide an improvement checklist
- Calculate the current word count
- Support academic integrity by analysing rather than writing the assignment

### Learning Analytics

- Record learning activities
- Display interaction statistics
- Visualise the use of questions, summaries, and quizzes
- Help students monitor learning engagement

### Active-Recall Study Planner

- Enter exam topics and available study hours
- Generate a structured study schedule
- Divide sessions into learning, recall, and practice
- Download the study plan as a CSV file

### Secure Local Authentication

- Local student registration and login
- Passwords protected using PBKDF2 hashing
- Random salts used for password storage
- Gemini API keys are not intentionally stored by the application

---

## How the System Works

```text
Student Question
       ↓
PDF Text Extraction and Cleaning
       ↓
Page-Preserving Document Chunking
       ↓
BM25 Keyword Retrieval
       +
FAISS Semantic Retrieval
       ↓
Hybrid Evidence Ranking
       ↓
Gemini Grounded Synthesis
       ↓
Answer with Page Citations
```

StudyPilot first searches the uploaded notes using two retrieval approaches:

1. **BM25 retrieval** identifies passages containing important keywords.
2. **FAISS semantic retrieval** identifies passages with similar meaning.

The results are combined and ranked before the selected evidence is provided to Gemini for a structured answer.

---

## Technology Stack

### Programming and Interface

- Python
- Streamlit
- Custom CSS animations and styling

### Artificial Intelligence and NLP

- Google Gemini API
- Sentence Transformers
- Natural Language Processing
- Retrieval-Augmented Generation

### Information Retrieval

- BM25 keyword search
- FAISS vector search
- Hybrid retrieval and ranking
- Semantic embeddings

### Document Processing

- PyMuPDF
- PDF text extraction
- Page metadata preservation
- Text cleaning and overlapping chunking

### Data and Analytics

- SQLite
- Pandas
- Plotly

### Development and Deployment

- Git
- GitHub
- Pytest
- Streamlit Community Cloud

---

## Project Structure

```text
studypilot-ai-ultimate/
│
├── .streamlit/
│   └── config.toml
│
├── src/
│   └── studypilot/
│       ├── __init__.py
│       ├── ai.py
│       ├── db.py
│       ├── documents.py
│       ├── models.py
│       └── retrieval.py
│
├── tests/
│   └── test_core.py
│
├── .env.example
├── .gitignore
├── app.py
├── pyproject.toml
├── requirements.txt
├── style.css
└── README.md
```

---

## Run the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/adeeshachathurmina-ux/studypilot-ai-ultimate.git
```

### 2. Open the project folder

```bash
cd studypilot-ai-ultimate
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment on Windows PowerShell

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.venv\Scripts\Activate.ps1
```

### 5. Install the dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Start the application

```bash
python -m streamlit run app.py
```

The local application will normally open in the browser through the Streamlit development server.

---

## Gemini API Configuration

A Gemini API key enables structured grounded answers, revision notes, quiz generation, past-paper analysis, and semantic assignment analysis.

The key can be entered directly into the password-protected field in the application sidebar.

Alternatively, create a local `.env` file based on `.env.example`:

```env
GEMINI_API_KEY=your_key_here
```

### API Key Security

- Never commit the `.env` file
- Never hard-code the key inside Python files
- Never publish the key in screenshots
- Never add a real key to `.env.example`
- Revoke the key immediately if it becomes public

The repository’s `.gitignore` file prevents common secret, database, environment, and cache files from being committed.

---

## Testing

Run the automated tests using:

```bash
python -m pytest
```

The current tests validate:

- PDF text cleaning
- Document chunk creation
- Core data-model behaviour

---

## Recommended Usage

For better results:

- Upload text-based PDFs rather than scanned image PDFs
- Upload notes from one module at a time
- Ask focused and specific questions
- Review the retrieved evidence
- Verify important information using the cited PDF pages
- Use lecturer-provided or otherwise authorised learning materials

Example question:

```text
What are the five main properties of an algorithm? Explain each property with a simple example.
```

---

## Responsible AI and Academic Integrity

StudyPilot AI Ultimate is designed as a learning-support tool.

The application should not be treated as a replacement for lecturers, official module materials, or independent academic judgement. AI-generated content can occasionally be incomplete or incorrect.

Students should:

- Verify answers using the displayed source pages
- Follow institutional academic-integrity policies
- Avoid submitting generated content as original assessed work
- Avoid uploading private, confidential, or unauthorised documents
- Use assignment analysis as guidance rather than automated grading

The application does not claim 100% accuracy.

---

## Current Limitations

- Scanned PDFs require OCR before they can be processed effectively
- Response quality depends on the quality of uploaded lecture notes
- Very large documents may require additional optimisation
- Generated answers depend on successful retrieval and Gemini availability
- Local SQLite accounts may not persist permanently on all cloud deployments
- The learning analytics module currently tracks application activity rather than full mastery of individual topics

---

## Future Improvements

- OCR support for scanned PDF documents
- Persistent cloud-based user accounts
- Topic-level knowledge-gap detection
- Interactive quiz marking and score tracking
- Multilingual explanations
- Downloadable revision-note documents
- Advanced past-paper topic-frequency analysis
- Retrieval quality evaluation dashboard
- Reranking models for improved evidence selection
- Mobile-focused interface improvements

---

## Repository Topics

```text
rag
generative-ai
data-science
natural-language-processing
semantic-search
faiss
bm25
streamlit
gemini-api
learning-analytics
education-technology
python
```

---

## Author

**MAC Oshadha**

Data Science Undergraduate  
NSBM Green University

---

## Project Links

- https://studypilot-ai-ultimate.streamlit.app/
- [GitHub Repository](https://github.com/adeeshachathurmina-ux/studypilot-ai-ultimate)

---

If this project is useful, consider giving the repository a star.
