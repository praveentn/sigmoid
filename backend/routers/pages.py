from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Cookie, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.auth import create_access_token, decode_token, verify_password
from backend.database import get_db
from backend.models import (
    AdminUser, Award, Certification, Education, Experience,
    ImpactMetric, Profile, Project, Research, Skill,
)

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
    profile = db.query(Profile).first()
    experience = db.query(Experience).order_by(Experience.order).all()
    education = db.query(Education).order_by(Education.order).all()
    skills = db.query(Skill).order_by(Skill.order).all()
    certifications = db.query(Certification).order_by(Certification.order).all()
    projects = db.query(Project).order_by(Project.order).all()
    research = db.query(Research).order_by(Research.order).all()
    awards = db.query(Award).order_by(Award.order).all()
    impact = db.query(ImpactMetric).order_by(ImpactMetric.order).all()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "profile": profile,
        "experience": experience,
        "education": education,
        "skills": skills,
        "certifications": certifications,
        "projects": projects,
        "research": research,
        "awards": awards,
        "impact": impact,
    })


# ── Admin auth ────────────────────────────────────────────────────────────────

@router.get("/admin", response_class=HTMLResponse)
def admin_login_page(request: Request, admin_token: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    if get_admin_user(admin_token, db):
        return RedirectResponse("/admin/dashboard", status_code=302)
    return templates.TemplateResponse("admin/login.html", {"request": request, "error": None})


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
            "admin/login.html",
            {"request": request, "error": "Invalid username or password"},
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
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
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
    return templates.TemplateResponse(f"admin/sections/{section}.html", {"request": request, **ctx})


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
    return templates.TemplateResponse("admin/sections/profile.html", {
        "request": request, "profile_data": p,
        "toast": "Profile saved successfully.",
    })


# ── Generic list-section helpers ──────────────────────────────────────────────

def _list_response(request, section, db, editing_id=None, adding=False, toast=None):
    ctx = _section_context(section, db)
    ctx.update({"request": request, "editing_id": editing_id, "adding": adding})
    if toast:
        ctx["toast"] = toast
    return templates.TemplateResponse(f"admin/sections/{section}.html", ctx)


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
