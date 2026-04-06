# 🔍 CrossLens

> Upload any document. Ask a question. Get evidence on **both sides** - not just the agreeable answer.

CrossLens is an advanced RAG (Retrieval-Augmented Generation) system that verifies claims against documents by finding supporting **and** contradicting evidence simultaneously. Unlike standard RAG chatbots that hallucinate by agreeing with users, CrossLens is deliberately skeptical.

## Key Architectural Pillars:

**Adaptive Routing** : Uses Gemini 1.5 Flash to classify queries as SIMPLE (greetings/summaries) or COMPLEX (verification), saving latency and cost.

**Multi-Vector Retrieval** : Simultaneously fires three distinct search queries (Supporting, Contradicting, Neutral) to ensure no stone is left unturned.

**Corrective RAG (CRAG)** : An automated Evaluator grades the relevance of local documents. If the local knowledge is insufficient, it triggers a Web Search fallback via DuckDuckGo.

**Agentic UI** : A professional Streamlit dashboard featuring real-time status logs, confidence metrics, and structured evidence tabs.

---

## 🚀 Live Demo

[🚀 Try CrossLens Live](https://cross-lens-advanced-rag.streamlit.app/)

---

## 🧠 How It Works

Most RAG systems find the most similar text to your query and call it an answer. CrossLens does something different, it runs three parallel searches, evaluates the quality of what it finds, and gives you a structured verdict with citations.

```
User uploads document + asks a query
        ↓
Adaptive Router → Simple / Complex / General?
        ↓
Multi-Vector Retrieval → searches for evidence FOR, AGAINST, and NEUTRAL
        ↓
CRAG Evaluator → grades chunk relevance → triggers web search if needed
        ↓
Generator → Structured verdict with citations
```

---

## ⚙️ Three Advanced RAG Concepts

### 1. Adaptive Routing
Not every query needs a heavy pipeline. A lightweight classifier routes each query:
- **SIMPLE** : document summary or explanation questions
- **COMPLEX** : claim verification, fact-checking
- **GENERAL** : unrelated to the document, triggers web search

### 2. Multi-Vector Retrieval
Instead of one search query, fires three in parallel:
- Supporting query : finds evidence FOR the claim
- Contradicting query : finds evidence AGAINST the claim
- Neutral query : finds ambiguous or nuanced statements

Results are merged and deduplicated before passing forward.

### 3. Corrective RAG (CRAG)
After retrieval, an evaluator grades chunk relevance before generation:
- **RELEVANT** → proceeds to generation
- **AMBIGUOUS** → supplements with web search
- **IRRELEVANT** → discards chunks, falls back to web search entirely

This eliminates the classic RAG failure of generating confident answers from garbage retrieved context.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq API (Llama 3.3 70B) |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) - local, free |
| Vector DB | ChromaDB - local |
| Pipeline | LangChain + LangGraph |
| Web Search Fallback | DDGS (DuckDuckGo) |
| Frontend | Streamlit |

**Cost to run: $0** - all embeddings and vector storage run locally.

---

## 📁 Project Structure

```
cross_lens/
├── .streamlit/
│   └── config.toml             ← Streamlit configuration
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── router.py           ← Adaptive routing logic
│   │   ├── retriever.py        ← Multi-vector retrieval
│   │   ├── evaluator.py        ← CRAG evaluator
│   │   ├── generator.py        ← Verdict generation
│   │   └── pipeline.py         ← Connects all stages
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── document_loader.py  ← PDF, DOCX, TXT parsing
│   │   └── embeddings.py       ← ChromaDB operations
│   └── __init__.py
├── tests/                      ← Component-level test scripts
├── main.py                     ← Streamlit app entry point
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## ⚡ Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/Yamini26284/cross_lens.git
cd cross_lens
```

**2. Create virtual environment**
```bash
uv venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

**3. Install dependencies**
```bash
uv pip install -r requirements.txt
```

**4. Set up environment variables**
```bash
cp .env.example .env
```
Add your Groq API key inside `.env`:
```
GROQ_API_KEY=your_key_here
```
Get a free key at [console.groq.com](https://console.groq.com)

**5. Run the app**
```bash
streamlit run main.py
```

---

## 👤 Author

**Yamini Priya M**
AI/ML Developer · LLM Applications · RAG Systems

[GitHub](https://github.com/Yamini26284) · [LinkedIn](https://linkedin.com/in/Yamini26284)