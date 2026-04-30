# sigmoid

Personal portfolio app for **Praveen T N** — Senior Technical Architect, Data & AI Global Practice.

Built with FastAPI + Jinja2 + HTMX. No frontend build step required.

---

## Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Templates**: Jinja2 (server-rendered HTML)
- **Admin UI**: HTMX (no JavaScript framework)
- **Deployment**: Railway (Python only, nixpacks)

---

## Local Development

### Requirements

- Python 3.12+
- PostgreSQL (or use SQLite for local dev via `DATABASE_URL=sqlite:///local.db`)

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

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string (Railway internal) |
| `DATABASE_PUBLIC_URL` | PostgreSQL connection string (public, for migrations) |
| `SECRET_KEY` | JWT signing secret |
| `ADMIN_PASSWORD` | Password for the `/admin` interface |

---

## Admin

Navigate to `/admin`, log in with username `admin` and the `ADMIN_PASSWORD` env var value.

The admin panel allows full CRUD on all portfolio sections: Profile, Experience, Education, Skills, Certifications, Projects, Research, Awards, and Impact Metrics.

---

## Deployment (Railway)

1. Push to GitHub.
2. Connect repo in Railway — it auto-detects Python via `nixpacks.toml`.
3. Add environment variables (`DATABASE_URL`, `SECRET_KEY`, `ADMIN_PASSWORD`).
4. Railway injects `PORT` automatically — do **not** set a custom target port.

The `Procfile` and `run.py` handle startup. Seed data is applied automatically on first boot.
