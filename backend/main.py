import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.database import Base, SessionLocal, engine
from backend.routers import auth, awards, certifications, education, experience, impact, profile, projects, research, skills
from backend.routers import pages
from backend.seed import run_seed

app = FastAPI(title="Praveen T N — Portfolio API", version="1.0.0", docs_url="/api/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JSON API routes
API_PREFIX = "/api/v1"
for router in [
    auth.router,
    profile.router,
    experience.router,
    education.router,
    skills.router,
    certifications.router,
    projects.router,
    research.router,
    awards.router,
    impact.router,
]:
    app.include_router(router, prefix=API_PREFIX)

# HTML page routes (Jinja2 + HTMX admin)
app.include_router(pages.router)

# Static files
STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()
