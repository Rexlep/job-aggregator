# Job Aggregator

A production-oriented job aggregation platform.

## Project Structure

- `backend/`: FastAPI application and SQLAlchemy database foundation
- `frontend/`: React and TypeScript application
- `docs/`: architecture and product documentation
- `docker-compose.yml`: local PostgreSQL and Redis services

Job scraping and source integrations are intentionally not implemented yet.

## Prerequisites

- Python 3.12+
- Node.js 20+
- Docker Desktop
- Git

## Local Setup

### Start infrastructure

```bash
docker compose up -d
```

### Backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000` and its OpenAPI documentation at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

The frontend is available at `http://localhost:5173`.

## Environment Variables

Root, backend and frontend `.env.example` files document the initial local configuration. Never commit real `.env` files or credentials.

## Development Principles

- Keep domain logic inside the backend and UI logic inside the frontend.
- Add source-specific collectors only after the common job schema is agreed.
- Prefer small modules over premature abstractions.
- Keep background ingestion independent from public API requests.
