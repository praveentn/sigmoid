import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.database import Base, SessionLocal, engine
from backend.routers import auth, awards, certifications, education, experience, impact, profile, projects, research, skills
from backend.seed import run_seed

app = FastAPI(title="Praveen T N — Portfolio API", version="1.0.0", docs_url="/api/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()


# Serve React frontend (production build)
FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"

if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_react(full_path: str):
        # Serve static files that exist
        candidate = FRONTEND_DIST / full_path
        if candidate.is_file():
            return FileResponse(str(candidate))
        # Fallback to index.html (SPA routing)
        return FileResponse(str(FRONTEND_DIST / "index.html"))
else:
    @app.get("/", include_in_schema=False)
    def root():
        return {"message": "API is running. Build the React frontend to see the UI."}
