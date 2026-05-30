# NegotiateIQ

**Live:** https://negotiatorai.streamlit.app

AI salary negotiation coach powered by Claude + real market data. Built with FastAPI, Supabase (pgvector), and Streamlit.

## What it does

- **Salary Negotiation** — Enter a job offer and get: market rate assessment, counter-offer range with exact numbers, a word-for-word negotiation email, and your key leverage points. Backed by a RAG pipeline over real NYC tech job descriptions and candidate profiles.
- **Negotiate Anything** — Rent, freelance rates, vendor contracts, job offers — describe your situation and get a ready-to-use script.
- **Data Ingestion** — Add job descriptions (text or PDF) and candidate profiles to grow the market database.

## Tech Stack

- **FastAPI** — REST API
- **Supabase + pgvector** — vector database for semantic similarity search
- **OpenAI text-embedding-3-small** — embeddings (1536 dimensions)
- **Claude (claude-sonnet-4-6)** — coaching and script generation
- **Streamlit** — frontend UI

## Setup

### 1. Clone and install

```bash
git clone <your-repo>
cd negotiateiq
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment variables

Create a `.env` file:

```env
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-proj-...
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

### 3. Supabase schema

Run `supabase/schema.sql` in your Supabase SQL editor. This creates:
- `job_descriptions` table with pgvector column
- `candidate_profiles` table with pgvector column
- `match_job_descriptions` and `match_candidate_profiles` RPC functions

### 4. Seed market data

```bash
python -m scripts.seed
```

Adds 8 NYC tech job descriptions (Ramp, Perplexity AI, Brex, Figma, Harvey AI, Spotify, Navan, Persona) and 5 candidate profiles with real negotiation outcomes.

## Running

**API server:**
```bash
uvicorn main:app --reload
```

**Streamlit frontend:**
```bash
streamlit run frontend/app.py
```

The API runs on `http://localhost:8000`. The frontend expects the API at that address by default (configurable via `API_URL` env var).

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/negotiate` | Salary negotiation coaching with RAG |
| POST | `/negotiate/free` | Negotiate anything (free-form) |
| POST | `/ingest/jd` | Ingest a job description (text) |
| POST | `/ingest/jd/pdf` | Ingest a job description (PDF upload) |
| POST | `/ingest/profile` | Ingest a candidate profile |
| POST | `/ingest/profile/pdf` | Ingest a resume PDF |
| GET | `/docs` | Interactive API docs (Swagger) |
