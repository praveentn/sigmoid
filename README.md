# sigmoid

Personal portfolio app for **Praveen T N** — Senior Technical Architect, Data & AI Global Practice.

Built with FastAPI + Jinja2 + HTMX. No frontend build step required.

---

## Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Templates**: Jinja2 (server-rendered HTML)
- **Styling**: Custom CSS (black/white/grey, enterprise design)
- **Interactivity**: HTMX + vanilla JS
- **AI Chat**: SIGMA chatbot — Gemini `gemini-flash-latest`
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
| `GEMINI_API_KEY` | Google AI Studio API key — powers SIGMA chatbot |

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
4. Set environment variables: `SECRET_KEY`, `ADMIN_PASSWORD`, `GEMINI_API_KEY`.
6. Railway injects `PORT` automatically — do **not** set a custom target port.

Seed data (full profile, 19 projects, skills, experience, wiki) is applied automatically on first boot.

---

## SIGMA Chatbot

SIGMA is a restricted AI assistant that answers questions about Praveen's career.

- **Backend**: Gemini `gemini-flash-latest` via Google AI Studio
- **Context**: Pulls relevant sections from the SIGMA Wiki (admin-editable)
- **Rate limit**: 20 queries per session per hour
- **Stop**: Users can abort generation mid-stream via the stop button
