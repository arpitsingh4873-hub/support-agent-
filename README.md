# Intelligent Customer Support Agent

A RAG-powered support bot that answers customer questions from company documents, handles multi-turn conversations, and escalates to human agents when needed.

## Features
- RAG pipeline — answers from your own documents (PDF, TXT)
- Multi-turn conversation memory
- Human escalation with Slack notifications
- Persistent conversation storage in PostgreSQL
- Streaming responses
- File upload endpoint
- React chat UI

## Tech Stack
- Python, FastAPI
- LangChain, Groq (LLaMA 3.1)
- ChromaDB (vector search)
- PostgreSQL (conversation storage)
- React (frontend)

## Setup

1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install: `pip install -r requirements.txt`
5. Add `.env` file with `GROQ_API_KEY`, `DATABASE_URL`, `SLACK_WEBHOOK_URL`
6. Run: `uvicorn app.main:app --reload`

## API Endpoints
- `POST /upload` — upload company documents
- `GET /chat` — chat with bot
- `GET /chat-stream` — streaming chat
- `GET /history/{session_id}` — view conversation history