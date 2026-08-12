# AI PetCare Assistant (Petco Summer Hackathon 2026)

A production-oriented multi-agent conversational AI that allows a pet parent to manage the complete pet-care journey from a single chat interface.

## 🌟 Features
- **Multi-Agent Orchestration**: CrewAI orchestrates specialized agents (Pet, Clinic, Appointment, Commerce) to solve user intents.
- **Deterministic API Boundaries**: LLMs handle reasoning; Python services handle factual retrieval and deterministic transactional mutations.
- **Safe Transactions**: Operations like booking an appointment or requesting a refill require explicit user confirmation via a State Machine.
- **RAG for FAQ**: Uses FAISS and OpenAI embeddings to accurately answer clinic policy questions.

## 🚀 Quick Start

### A. Installation
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### B. Configuration
1. Copy `.env.example` to `.env`.
2. Add your `OPENAI_API_KEY`.

### C. Run the Application
You can run locally with Uvicorn or using Docker.

**Docker (Recommended)**
```bash
docker-compose up --build
```

**Local Run**
```bash
uvicorn app.main:app --reload
```

### D. Swagger UI
Access the interactive API documentation at:
http://localhost:8000/docs

### E. Ingesting FAQ Documents for RAG
```bash
python scripts/ingest_faq.py
```

## 💬 Example Demo Scenarios

**1. Find a vet near me and book an appointment**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/chat' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "USER-1001",
  "message": "Find a vet near me for Max and what are the available slots?"
}'
```
*The system will query clinics, find slots, and ask for confirmation to book.*

**2. Confirming the booking**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/chat' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "USER-1001",
  "message": "Yes, book the 10:30 AM slot."
}'
```
*The system hits the deterministic `book_appointment` service.*

## 🏗️ Architecture Note
Mock data is stored in `data/*.json`. Services in `app/services/` wrap this data. To transition to production, simply inject `httpx` API clients into these services to hit real Petco Enterprise APIs. The Agent logic remains completely unchanged.
# ai_petcare_assistant
