# sigmoid

Personal portfolio app for **Praveen T N** — Senior Technical Architect, Data & AI Global Practice.

Built with FastAPI + Jinja2 + HTMX. No frontend build step required.

---

## Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Templates**: Jinja2 (server-rendered HTML)
- **Styling**: Custom CSS (black/white/grey, enterprise design)
- **Interactivity**: HTMX + vanilla JS
- **AI Chat**: SIGMA chatbot — Gemini `gemini-2.0-flash` (primary) + Ollama (fallback)
- **Deployment**: Railway (Python only, nixpacks)

---

## Features

- Animated hero with live decimal years-of-experience counter (from March 2010)
- Experience accordion, project filter by category and company
- Ctrl+K search overlay across projects, experience, skills, research
- SIGMA AI chatbot (bottom-right) — queries Praveen's career knowledge base
- Contact form (stored in DB, visible in admin)
- SIGMA Wiki — admin-only markdown knowledge base that feeds SIGMA's context
- Full admin panel at `/admin` — CRUD for all sections + wiki editor + contact inbox

---

## Local Development

### Requirements

- Python 3.12+
- PostgreSQL (or SQLite for local dev via `DATABASE_URL=sqlite:///local.db`)

### Setup

**Windows:**
```
start.bat
```

**Linux / Mac:**
```
chmod +x start.sh
./start.sh
```

The script creates a virtualenv, installs dependencies, and starts the server.

- App: http://localhost:8000
- Admin: http://localhost:8000/admin
- API docs: http://localhost:8000/api/docs

---

## Environment Variables

### Required

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string (Railway internal URL) |
| `SECRET_KEY` | JWT signing secret (long random string) |
| `ADMIN_PASSWORD` | Password for the `/admin` interface |
| `GEMINI_API_KEY` | Google AI Studio API key — primary SIGMA backend |

### Ollama (fallback AI — optional but recommended)

| Variable | Description | Default |
|---|---|---|
| `OLLAMA_BASE_URL` | URL of running Ollama server | set by `run.py` at startup |
| `OLLAMA_MODEL` | Model name to use and pull on first boot | `phi3:mini` |
| `OLLAMA_MODELS` | Directory to store downloaded models | `/models` |

On Railway, attach a persistent volume at `/models` to cache the model across deploys.

`run.py` downloads the Ollama binary automatically at startup and starts the server.
On first boot it pulls `OLLAMA_MODEL` into the volume. Subsequent boots skip the download.

If the auto-pull fails (e.g. incorrect model name), SSH into the Railway container and run:
```bash
OLLAMA_MODELS=/models /app/ollama pull <model-name>
```

### Railway-injected (do not set manually)

| Variable | Description |
|---|---|
| `PORT` | Injected by Railway — do not override |

---

## Admin

Navigate to `/admin`, log in with username `admin` and the `ADMIN_PASSWORD` value.

Sections managed via admin:
- Profile, Experience, Education, Skills, Certifications
- Projects, Research, Awards, Impact Metrics
- **SIGMA Wiki** — markdown knowledge base for the chatbot
- **Contact Inbox** — view and manage contact form submissions

---

## Deployment (Railway)

1. Push to GitHub.
2. Connect repo in Railway — auto-detected via `nixpacks.toml`.
3. Add a PostgreSQL plugin — `DATABASE_URL` is injected automatically.
4. Add a persistent volume mounted at `/models` (for Ollama model cache).
5. Set environment variables: `SECRET_KEY`, `ADMIN_PASSWORD`, `GEMINI_API_KEY`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL`.
6. Railway injects `PORT` automatically — do **not** set a custom target port.

Seed data (full profile, 19 projects, skills, experience, wiki) is applied automatically on first boot.

---

## SIGMA Chatbot

SIGMA is a restricted AI assistant that answers questions about Praveen's career.

- **Primary**: Gemini `gemini-2.0-flash` via Google AI Studio (free tier)
- **Fallback**: Ollama local model when Gemini quota is exceeded
- **Context**: Pulls relevant sections from the SIGMA Wiki (admin-editable)
- **Rate limit**: 20 queries per session per hour
- **Stop**: Users can abort generation mid-stream via the stop button
