import os
import time
from collections import defaultdict
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Cookie, Depends, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.auth import create_access_token, decode_token, verify_password
from backend.database import get_db
from backend.models import (
    AdminUser, Award, Certification, ContactSubmission, Education, Experience,
    ImpactMetric, Profile, Project, Research, Skill, Wiki,
)

# ── Rate limiter (in-memory, per session_id) ──────────────────────────────────
_rate_buckets: dict = defaultdict(lambda: {"count": 0, "reset_at": 0})
_RATE_MAX = 20
_RATE_WINDOW = 3600  # 1 hour

def _rl_check(key: str) -> tuple[bool, int]:
    now = time.time()
    b = _rate_buckets[key]
    if b["reset_at"] < now:
        b["count"] = 0
        b["reset_at"] = now + _RATE_WINDOW
    b["count"] += 1
    remaining = max(0, _RATE_MAX - b["count"])
    return b["count"] <= _RATE_MAX, remaining

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter(tags=["pages"])


# ── Auth helpers ──────────────────────────────────────────────────────────────

def get_admin_user(admin_token: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    if not admin_token:
        return None
    username = decode_token(admin_token)
    if not username:
        return None
    return db.query(AdminUser).filter(AdminUser.username == username).first()


def require_admin(admin_token: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    user = get_admin_user(admin_token, db)
    if not user:
        raise _redirect_to_login()
    return user


def _redirect_to_login():
    return RedirectResponse("/admin", status_code=302)


def _htmx_auth_error():
    r = HTMLResponse("Unauthorized", status_code=401)
    r.headers["HX-Redirect"] = "/admin"
    return r


# ── Public page ───────────────────────────────────────────────────────────────

@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    import json as _json
    profile = db.query(Profile).first()
    experience = db.query(Experience).order_by(Experience.order).all()
    education = db.query(Education).order_by(Education.order).all()
    skills = db.query(Skill).order_by(Skill.order).all()
    certifications = db.query(Certification).order_by(Certification.order).all()
    projects = db.query(Project).order_by(Project.order).all()
    research = db.query(Research).order_by(Research.order).all()
    awards = db.query(Award).order_by(Award.order).all()
    impact = db.query(ImpactMetric).order_by(ImpactMetric.order).all()

    # Build search index JSON for client-side search
    search_index = _json.dumps({
        "projects": [{"id": p.id, "name": p.name, "description": p.description or "",
                       "tech": p.tech_stack or [], "company": p.company or "",
                       "category": p.category or "", "type": "project"} for p in projects],
        "experience": [{"id": e.id, "company": e.company, "role": e.role,
                         "highlights": e.highlights or [], "type": "experience"} for e in experience],
        "skills": [{"id": s.id, "category": s.category, "items": s.items or [], "type": "skill"} for s in skills],
        "research": [{"id": r.id, "title": r.title, "description": r.description or "",
                       "focus_area": r.focus_area or "", "type": "research"} for r in research],
    })

    return templates.TemplateResponse(request, "index.html", {
        "profile": profile,
        "experience": experience,
        "education": education,
        "skills": skills,
        "certifications": certifications,
        "projects": projects,
        "research": research,
        "awards": awards,
        "impact": impact,
        "search_index_json": search_index,
    })


# ── Admin auth ────────────────────────────────────────────────────────────────

@router.get("/admin", response_class=HTMLResponse)
def admin_login_page(request: Request, admin_token: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    if get_admin_user(admin_token, db):
        return RedirectResponse("/admin/dashboard", status_code=302)
    return templates.TemplateResponse(request, "admin/login.html", {"error": None})


@router.post("/admin/login")
def admin_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(AdminUser).filter(AdminUser.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            request, "admin/login.html",
            {"error": "Invalid username or password"},
            status_code=401,
        )
    token = create_access_token({"sub": username})
    response = RedirectResponse("/admin/dashboard", status_code=302)
    response.set_cookie("admin_token", token, httponly=True, samesite="lax", max_age=86400)
    return response


@router.get("/admin/logout")
def admin_logout():
    response = RedirectResponse("/admin", status_code=302)
    response.delete_cookie("admin_token")
    return response


# ── Admin dashboard ───────────────────────────────────────────────────────────

@router.get("/admin/dashboard", response_class=HTMLResponse)
def admin_dashboard(
    request: Request,
    section: str = "profile",
    db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
):
    user = get_admin_user(admin_token, db)
    if not user:
        return RedirectResponse("/admin", status_code=302)
    ctx = _section_context(section, db)
    return templates.TemplateResponse(request, "admin/dashboard.html", {
        "user": user,
        "active_section": section,
        **ctx,
    })


# ── Admin section partials (HTMX) ─────────────────────────────────────────────

def _section_context(section: str, db: Session) -> dict:
    """Load data for the active admin section."""
    if section == "profile":
        return {"profile_data": db.query(Profile).first()}
    if section == "impact":
        return {"items": db.query(ImpactMetric).order_by(ImpactMetric.order).all(), "editing_id": None, "adding": False}
    if section == "experience":
        return {"items": db.query(Experience).order_by(Experience.order).all(), "editing_id": None, "adding": False}
    if section == "education":
        return {"items": db.query(Education).order_by(Education.order).all(), "editing_id": None, "adding": False}
    if section == "skills":
        return {"items": db.query(Skill).order_by(Skill.order).all(), "editing_id": None, "adding": False}
    if section == "certifications":
        return {"items": db.query(Certification).order_by(Certification.order).all(), "editing_id": None, "adding": False}
    if section == "projects":
        return {"items": db.query(Project).order_by(Project.order).all(), "editing_id": None, "adding": False}
    if section == "research":
        return {"items": db.query(Research).order_by(Research.order).all(), "editing_id": None, "adding": False}
    if section == "awards":
        return {"items": db.query(Award).order_by(Award.order).all(), "editing_id": None, "adding": False}
    if section == "wiki":
        return {"wiki": db.query(Wiki).first()}
    if section == "contact":
        return {"items": db.query(ContactSubmission).order_by(ContactSubmission.submitted_at.desc()).all()}
    return {}


@router.get("/admin/section/{section}", response_class=HTMLResponse)
def admin_section(
    request: Request,
    section: str,
    db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    ctx = _section_context(section, db)
    return templates.TemplateResponse(request, f"admin/sections/{section}.html", ctx)


# ── Profile ───────────────────────────────────────────────────────────────────

@router.post("/admin/section/profile", response_class=HTMLResponse)
def save_profile(
    request: Request,
    db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    name: str = Form(""),
    title: str = Form(""),
    company: str = Form(""),
    tagline: str = Form(""),
    bio: str = Form(""),
    email: str = Form(""),
    phone: str = Form(""),
    location: str = Form(""),
    linkedin_url: str = Form(""),
    credly_url: str = Form(""),
    visa_info: str = Form(""),
    years_experience: str = Form(""),
    solutions_delivered: str = Form(""),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    p = db.query(Profile).first()
    if p:
        p.name = name; p.title = title; p.company = company
        p.tagline = tagline; p.bio = bio; p.email = email
        p.phone = phone; p.location = location
        p.linkedin_url = linkedin_url; p.credly_url = credly_url
        p.visa_info = visa_info
        p.years_experience = int(years_experience) if years_experience.isdigit() else p.years_experience
        p.solutions_delivered = int(solutions_delivered) if solutions_delivered.isdigit() else p.solutions_delivered
        db.commit(); db.refresh(p)
    return templates.TemplateResponse(request, "admin/sections/profile.html", {
        "profile_data": p,
        "toast": "Profile saved successfully.",
    })


# ── Generic list-section helpers ──────────────────────────────────────────────

def _list_response(request, section, db, editing_id=None, adding=False, toast=None):
    ctx = _section_context(section, db)
    ctx.update({"editing_id": editing_id, "adding": adding})
    if toast:
        ctx["toast"] = toast
    return templates.TemplateResponse(request, f"admin/sections/{section}.html", ctx)


# ── Experience ────────────────────────────────────────────────────────────────

@router.post("/admin/section/experience", response_class=HTMLResponse)
def create_experience(
    request: Request, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    company: str = Form(""), role: str = Form(""),
    period_start: str = Form(""), period_end: str = Form(""),
    location: str = Form(""), tagline: str = Form(""),
    highlights: str = Form(""), is_current: str = Form(""),
    order: str = Form("0"),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    db.add(Experience(
        company=company, role=role, period_start=period_start, period_end=period_end,
        location=location, tagline=tagline,
        highlights=[h.strip() for h in highlights.splitlines() if h.strip()],
        is_current=is_current == "on", order=int(order) if order.isdigit() else 0,
    ))
    db.commit()
    return _list_response(request, "experience", db, toast="Entry added.")


@router.post("/admin/section/experience/{item_id}", response_class=HTMLResponse)
def update_experience(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    company: str = Form(""), role: str = Form(""),
    period_start: str = Form(""), period_end: str = Form(""),
    location: str = Form(""), tagline: str = Form(""),
    highlights: str = Form(""), is_current: str = Form(""),
    order: str = Form("0"),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(Experience).filter(Experience.id == item_id).first()
    if item:
        item.company = company; item.role = role
        item.period_start = period_start; item.period_end = period_end
        item.location = location; item.tagline = tagline
        item.highlights = [h.strip() for h in highlights.splitlines() if h.strip()]
        item.is_current = is_current == "on"
        item.order = int(order) if order.isdigit() else 0
        db.commit()
    return _list_response(request, "experience", db, toast="Saved.")


@router.post("/admin/section/experience/{item_id}/delete", response_class=HTMLResponse)
def delete_experience(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(Experience).filter(Experience.id == item_id).first()
    if item:
        db.delete(item); db.commit()
    return _list_response(request, "experience", db, toast="Deleted.")


# ── Education ─────────────────────────────────────────────────────────────────

@router.post("/admin/section/education", response_class=HTMLResponse)
def create_education(
    request: Request, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    institution: str = Form(""), degree: str = Form(""),
    year: str = Form(""), description: str = Form(""), order: str = Form("0"),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    db.add(Education(institution=institution, degree=degree, year=year, description=description, order=int(order) if order.isdigit() else 0))
    db.commit()
    return _list_response(request, "education", db, toast="Added.")


@router.post("/admin/section/education/{item_id}", response_class=HTMLResponse)
def update_education(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    institution: str = Form(""), degree: str = Form(""),
    year: str = Form(""), description: str = Form(""), order: str = Form("0"),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(Education).filter(Education.id == item_id).first()
    if item:
        item.institution = institution; item.degree = degree
        item.year = year; item.description = description
        item.order = int(order) if order.isdigit() else 0
        db.commit()
    return _list_response(request, "education", db, toast="Saved.")


@router.post("/admin/section/education/{item_id}/delete", response_class=HTMLResponse)
def delete_education(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(Education).filter(Education.id == item_id).first()
    if item:
        db.delete(item); db.commit()
    return _list_response(request, "education", db, toast="Deleted.")


# ── Skills ────────────────────────────────────────────────────────────────────

@router.post("/admin/section/skills", response_class=HTMLResponse)
def create_skill(
    request: Request, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    category: str = Form(""), items_text: str = Form(""), order: str = Form("0"),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    db.add(Skill(category=category, items=[i.strip() for i in items_text.split(",") if i.strip()], order=int(order) if order.isdigit() else 0))
    db.commit()
    return _list_response(request, "skills", db, toast="Added.")


@router.post("/admin/section/skills/{item_id}", response_class=HTMLResponse)
def update_skill(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    category: str = Form(""), items_text: str = Form(""), order: str = Form("0"),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(Skill).filter(Skill.id == item_id).first()
    if item:
        item.category = category
        item.items = [i.strip() for i in items_text.split(",") if i.strip()]
        item.order = int(order) if order.isdigit() else 0
        db.commit()
    return _list_response(request, "skills", db, toast="Saved.")


@router.post("/admin/section/skills/{item_id}/delete", response_class=HTMLResponse)
def delete_skill(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(Skill).filter(Skill.id == item_id).first()
    if item:
        db.delete(item); db.commit()
    return _list_response(request, "skills", db, toast="Deleted.")


# ── Certifications ────────────────────────────────────────────────────────────

@router.post("/admin/section/certifications", response_class=HTMLResponse)
def create_certification(
    request: Request, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    name: str = Form(""), issuer: str = Form(""), year: str = Form(""),
    is_featured: str = Form(""), order: str = Form("0"),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    db.add(Certification(name=name, issuer=issuer, year=year, is_featured=is_featured == "on", order=int(order) if order.isdigit() else 0))
    db.commit()
    return _list_response(request, "certifications", db, toast="Added.")


@router.post("/admin/section/certifications/{item_id}", response_class=HTMLResponse)
def update_certification(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    name: str = Form(""), issuer: str = Form(""), year: str = Form(""),
    is_featured: str = Form(""), order: str = Form("0"),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(Certification).filter(Certification.id == item_id).first()
    if item:
        item.name = name; item.issuer = issuer; item.year = year
        item.is_featured = is_featured == "on"
        item.order = int(order) if order.isdigit() else 0
        db.commit()
    return _list_response(request, "certifications", db, toast="Saved.")


@router.post("/admin/section/certifications/{item_id}/delete", response_class=HTMLResponse)
def delete_certification(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(Certification).filter(Certification.id == item_id).first()
    if item:
        db.delete(item); db.commit()
    return _list_response(request, "certifications", db, toast="Deleted.")


# ── Projects ──────────────────────────────────────────────────────────────────

@router.post("/admin/section/projects", response_class=HTMLResponse)
def create_project(
    request: Request, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    name: str = Form(""), description: str = Form(""),
    tech_text: str = Form(""), period: str = Form(""),
    category: str = Form(""), company: str = Form(""),
    role: str = Form(""), highlights: str = Form(""),
    is_featured: str = Form(""), order: str = Form("0"),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    db.add(Project(
        name=name, description=description,
        tech_stack=[t.strip() for t in tech_text.split(",") if t.strip()],
        period=period, category=category, company=company, role=role,
        highlights=[h.strip() for h in highlights.splitlines() if h.strip()],
        is_featured=is_featured == "on", order=int(order) if order.isdigit() else 0,
    ))
    db.commit()
    return _list_response(request, "projects", db, toast="Added.")


@router.post("/admin/section/projects/{item_id}", response_class=HTMLResponse)
def update_project(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    name: str = Form(""), description: str = Form(""),
    tech_text: str = Form(""), period: str = Form(""),
    category: str = Form(""), company: str = Form(""),
    role: str = Form(""), highlights: str = Form(""),
    is_featured: str = Form(""), order: str = Form("0"),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(Project).filter(Project.id == item_id).first()
    if item:
        item.name = name; item.description = description
        item.tech_stack = [t.strip() for t in tech_text.split(",") if t.strip()]
        item.period = period; item.category = category
        item.company = company; item.role = role
        item.highlights = [h.strip() for h in highlights.splitlines() if h.strip()]
        item.is_featured = is_featured == "on"
        item.order = int(order) if order.isdigit() else 0
        db.commit()
    return _list_response(request, "projects", db, toast="Saved.")


@router.post("/admin/section/projects/{item_id}/delete", response_class=HTMLResponse)
def delete_project(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(Project).filter(Project.id == item_id).first()
    if item:
        db.delete(item); db.commit()
    return _list_response(request, "projects", db, toast="Deleted.")


# ── Research ──────────────────────────────────────────────────────────────────

@router.post("/admin/section/research", response_class=HTMLResponse)
def create_research(
    request: Request, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    title: str = Form(""), description: str = Form(""),
    type: str = Form("publication"), focus_area: str = Form(""), order: str = Form("0"),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    db.add(Research(title=title, description=description, type=type, focus_area=focus_area, order=int(order) if order.isdigit() else 0))
    db.commit()
    return _list_response(request, "research", db, toast="Added.")


@router.post("/admin/section/research/{item_id}", response_class=HTMLResponse)
def update_research(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    title: str = Form(""), description: str = Form(""),
    type: str = Form("publication"), focus_area: str = Form(""), order: str = Form("0"),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(Research).filter(Research.id == item_id).first()
    if item:
        item.title = title; item.description = description
        item.type = type; item.focus_area = focus_area
        item.order = int(order) if order.isdigit() else 0
        db.commit()
    return _list_response(request, "research", db, toast="Saved.")


@router.post("/admin/section/research/{item_id}/delete", response_class=HTMLResponse)
def delete_research(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(Research).filter(Research.id == item_id).first()
    if item:
        db.delete(item); db.commit()
    return _list_response(request, "research", db, toast="Deleted.")


# ── Awards ────────────────────────────────────────────────────────────────────

@router.post("/admin/section/awards", response_class=HTMLResponse)
def create_award(
    request: Request, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    title: str = Form(""), description: str = Form(""),
    year: str = Form(""), organization: str = Form(""), order: str = Form("0"),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    db.add(Award(title=title, description=description, year=year, organization=organization, order=int(order) if order.isdigit() else 0))
    db.commit()
    return _list_response(request, "awards", db, toast="Added.")


@router.post("/admin/section/awards/{item_id}", response_class=HTMLResponse)
def update_award(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    title: str = Form(""), description: str = Form(""),
    year: str = Form(""), organization: str = Form(""), order: str = Form("0"),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(Award).filter(Award.id == item_id).first()
    if item:
        item.title = title; item.description = description
        item.year = year; item.organization = organization
        item.order = int(order) if order.isdigit() else 0
        db.commit()
    return _list_response(request, "awards", db, toast="Saved.")


@router.post("/admin/section/awards/{item_id}/delete", response_class=HTMLResponse)
def delete_award(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(Award).filter(Award.id == item_id).first()
    if item:
        db.delete(item); db.commit()
    return _list_response(request, "awards", db, toast="Deleted.")


# ── Impact Metrics ────────────────────────────────────────────────────────────

@router.post("/admin/section/impact", response_class=HTMLResponse)
def create_impact(
    request: Request, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    metric: str = Form(""), label: str = Form(""),
    description: str = Form(""), order: str = Form("0"),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    db.add(ImpactMetric(metric=metric, label=label, description=description, order=int(order) if order.isdigit() else 0))
    db.commit()
    return _list_response(request, "impact", db, toast="Added.")


@router.post("/admin/section/impact/{item_id}", response_class=HTMLResponse)
def update_impact(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    metric: str = Form(""), label: str = Form(""),
    description: str = Form(""), order: str = Form("0"),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(ImpactMetric).filter(ImpactMetric.id == item_id).first()
    if item:
        item.metric = metric; item.label = label
        item.description = description
        item.order = int(order) if order.isdigit() else 0
        db.commit()
    return _list_response(request, "impact", db, toast="Saved.")


@router.post("/admin/section/impact/{item_id}/delete", response_class=HTMLResponse)
def delete_impact(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(ImpactMetric).filter(ImpactMetric.id == item_id).first()
    if item:
        db.delete(item); db.commit()
    return _list_response(request, "impact", db, toast="Deleted.")


# ── Contact form (public) ─────────────────────────────────────────────────────

@router.post("/contact", response_class=HTMLResponse)
def submit_contact(
    request: Request, db: Session = Depends(get_db),
    name: str = Form(""), email: str = Form(""),
    subject: str = Form(""), message: str = Form(""),
):
    if name.strip() and email.strip() and message.strip():
        db.add(ContactSubmission(
            name=name.strip(), email=email.strip(),
            subject=subject.strip(), message=message.strip(),
        ))
        db.commit()
    return HTMLResponse("""
<div class="contact-success">
  <div class="contact-success-icon">✓</div>
  <div class="contact-success-title">Message received.</div>
  <p>I'll review your message and get back to you. Thank you for reaching out.</p>
</div>
""")


# ── SIGMA Chat (public) ───────────────────────────────────────────────────────

def _parse_wiki_sections(content: str) -> list[tuple[str, str]]:
    """Parse markdown wiki into [(heading, body)] by ## / ### headings."""
    sections: list[tuple[str, str]] = []
    current_heading = "Overview"
    current_lines: list[str] = []
    for line in content.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("## ") or stripped.startswith("### "):
            if current_lines:
                sections.append((current_heading, "\n".join(current_lines).strip()))
            current_heading = stripped.lstrip("#").strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_lines:
        sections.append((current_heading, "\n".join(current_lines).strip()))
    return sections


_STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "what", "when", "where",
    "who", "how", "did", "does", "do", "i", "me", "his", "her", "their",
    "about", "tell", "can", "you", "he", "she", "they", "it", "in", "on",
    "at", "for", "with", "and", "or", "of", "to", "from", "has", "have",
    "been", "be", "will", "would", "could", "should", "please", "give",
}


def _relevant_wiki_context(wiki_content: str, query: str, max_chars: int = 2500) -> str:
    """Select the most relevant wiki sections for a given query (no full-dump)."""
    sections = _parse_wiki_sections(wiki_content)
    if not sections:
        return wiki_content[:max_chars]

    terms = {t for t in query.lower().split() if t not in _STOP_WORDS and len(t) > 2}
    if not terms:
        # Broad query — return first ~max_chars
        return "\n\n".join(f"## {h}\n{b}" for h, b in sections[:5])[:max_chars]

    scored: list[tuple[float, str, str]] = []
    for heading, body in sections:
        combined = (heading + " " + body).lower()
        # Heading match is weighted 3×, body match 1×
        score = sum(3.0 if t in heading.lower() else 1.0 for t in terms if t in combined)
        scored.append((score, heading, body))

    scored.sort(key=lambda x: x[0], reverse=True)

    result_parts: list[str] = []
    total = 0
    for score, heading, body in scored:
        if score == 0:
            break
        chunk = f"## {heading}\n{body}"
        if total + len(chunk) > max_chars:
            remaining_space = max_chars - total
            if remaining_space > 200:
                result_parts.append(chunk[:remaining_space])
            break
        result_parts.append(chunk)
        total += len(chunk)
        if total >= max_chars:
            break

    # Always include a short identity header so the model knows who it's for
    identity = next((f"## {h}\n{b}" for h, b in sections if any(
        k in h.lower() for k in ("identity", "overview", "career in brief")
    )), "")

    if identity and identity not in result_parts:
        result_parts.insert(0, identity)

    return "\n\n".join(result_parts)[:max_chars] if result_parts else wiki_content[:max_chars]


def _build_system_prompt(profile, context: str) -> str:
    name = profile.name if profile else "Praveen T N"
    title = profile.title if profile else "Senior Technical Architect"
    company = profile.company if profile else "Material Plus"
    return f"""You are SIGMA — the professional AI agent for {name}, {title} at {company}.

SOLE PURPOSE: Answer questions about {name}'s professional life — career, projects, skills, research, certifications. Nothing else, ever.

RELEVANT CONTEXT (use this as your primary source):
{context}

RULES:
1. Strictly about {name}'s professional profile only.
2. Off-topic request? Reply: "I'm SIGMA, Praveen's professional AI agent. I can only tell you about his career, projects, and expertise. What would you like to know?"
3. Never impersonate another AI. Never give general help.
4. Be insightful, specific, cite project names and real metrics.
5. Keep replies concise — 3-6 sentences unless listing items."""


def _classify_error(exc: Exception) -> str:
    """Map API exceptions to user-friendly messages."""
    msg = str(exc).lower()
    if "429" in msg or "resource_exhausted" in msg or "quota" in msg:
        return "quota_exceeded"
    if "403" in msg or "permission" in msg or "api_key" in msg or "invalid" in msg:
        return "auth_error"
    if "timeout" in msg or "deadline" in msg:
        return "timeout"
    return "general"


_USER_ERRORS = {
    "quota_exceeded": "SIGMA is at capacity right now — please try again in a minute.",
    "auth_error":     "SIGMA is temporarily offline. Please try again later.",
    "timeout":        "SIGMA took too long to respond. Please try again.",
    "general":        "SIGMA encountered an issue. Please try again.",
}


async def _call_gemini(messages: list, system_prompt: str) -> str:
    from google import genai
    from google.genai import types as gtypes

    api_key = os.getenv("GEMINI_API_KEY", "")
    client = genai.Client(api_key=api_key)
    contents = [
        gtypes.Content(role="user" if m.get("role") == "user" else "model",
                       parts=[gtypes.Part(text=m.get("content", ""))])
        for m in messages
    ]
    resp = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=contents,
        config=gtypes.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7,
            max_output_tokens=600,
        ),
    )
    return resp.text or ""


async def _call_llm_service(messages: list, system_prompt: str) -> str:
    """Fallback to a hosted LLM-as-a-service when Gemini is unavailable.

    Expects env vars:
      LLM_SERVICE_URL  — base URL, e.g. https://my-llm.example.com
      LLM_SERVICE_KEY  — Bearer token for Authorization header
      LLM_SERVICE_MODEL — model name to pass in the request body (optional)
    Calls POST {LLM_SERVICE_URL}/api/generate
    """
    import json as _json
    import urllib.request as _urlreq

    base_url = os.getenv("LLM_SERVICE_URL", "").rstrip("/")
    api_key = os.getenv("LLM_SERVICE_KEY", "")
    model = os.getenv("LLM_SERVICE_MODEL", "")

    # Flatten conversation into a single prompt for /api/generate
    history = "\n".join(
        f"{'User' if m.get('role') == 'user' else 'Assistant'}: {m.get('content', '')}"
        for m in messages
    )
    prompt = f"{system_prompt}\n\n{history}\nAssistant:"

    payload = _json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 600},
    }).encode()

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = _urlreq.Request(f"{base_url}/api/generate", data=payload, headers=headers)
    with _urlreq.urlopen(req, timeout=30) as r:
        data = _json.loads(r.read())
    return (data.get("response") or data.get("content") or "").strip()


@router.post("/api/chat")
async def chat(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid request"}, status_code=400)

    messages = data.get("messages", [])
    session_id = data.get("session_id") or (request.client.host if request.client else "anon")

    allowed, remaining = _rl_check(session_id)
    if not allowed:
        return JSONResponse({"error": "You've reached today's query limit. Come back later.",
                             "remaining": 0, "blocked": True}, status_code=429)

    if not os.getenv("GEMINI_API_KEY") and not os.getenv("LLM_SERVICE_URL"):
        return JSONResponse({"error": "SIGMA is offline — no AI backend configured.",
                             "remaining": remaining}, status_code=503)

    # Build context from wiki using relevance extraction
    wiki = db.query(Wiki).first()
    raw_wiki = wiki.content if wiki else ""
    last_user_q = next((m["content"] for m in reversed(messages) if m.get("role") == "user"), "")
    context = _relevant_wiki_context(raw_wiki, last_user_q) if raw_wiki else ""
    profile = db.query(Profile).first()
    system_prompt = _build_system_prompt(profile, context)

    reply = ""
    gemini_err: Exception | None = None

    # Try Gemini first
    if os.getenv("GEMINI_API_KEY"):
        try:
            reply = await _call_gemini(messages, system_prompt)
        except Exception as e:
            gemini_err = e
            print(f"[gemini] error: {e}")

    # Fallback to hosted LLM service
    llm_err = None
    if not reply and os.getenv("LLM_SERVICE_URL"):
        try:
            reply = await _call_llm_service(messages, system_prompt)
        except Exception as e:
            llm_err = e
            print(f"[llm_service] fallback error: {e}")

    if not reply:
        if llm_err is not None:
            err_key = "general"
        else:
            err_key = _classify_error(gemini_err) if gemini_err else "general"
        return JSONResponse({"error": _USER_ERRORS[err_key], "remaining": remaining}, status_code=503)

    return JSONResponse({"reply": reply, "remaining": remaining, "blocked": False})


# ── Wiki admin ────────────────────────────────────────────────────────────────

@router.post("/admin/section/wiki", response_class=HTMLResponse)
def save_wiki(
    request: Request, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
    content: str = Form(""),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    wiki = db.query(Wiki).first()
    if wiki:
        wiki.content = content
    else:
        db.add(Wiki(content=content))
    db.commit()
    wiki = db.query(Wiki).first()
    return templates.TemplateResponse(request, "admin/sections/wiki.html", {
        "wiki": wiki, "toast": "Wiki saved."
    })


# ── Contact admin ─────────────────────────────────────────────────────────────

@router.post("/admin/section/contact/{item_id}/read", response_class=HTMLResponse)
def mark_contact_read(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(ContactSubmission).filter(ContactSubmission.id == item_id).first()
    if item:
        item.is_read = True; db.commit()
    return _list_response(request, "contact", db)


@router.post("/admin/section/contact/{item_id}/delete", response_class=HTMLResponse)
def delete_contact(
    request: Request, item_id: int, db: Session = Depends(get_db),
    admin_token: Optional[str] = Cookie(None),
):
    if not get_admin_user(admin_token, db):
        return _htmx_auth_error()
    item = db.query(ContactSubmission).filter(ContactSubmission.id == item_id).first()
    if item:
        db.delete(item); db.commit()
    return _list_response(request, "contact", db, toast="Deleted.")
