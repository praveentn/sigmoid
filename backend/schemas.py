from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


# --- Profile ---

class ProfileBase(BaseModel):
    name: str
    title: Optional[str] = None
    company: Optional[str] = None
    tagline: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    credly_url: Optional[str] = None
    visa_info: Optional[str] = None
    years_experience: Optional[int] = None
    solutions_delivered: Optional[int] = None
    photo_url: Optional[str] = None


class ProfileUpdate(ProfileBase):
    name: Optional[str] = None


class ProfileResponse(ProfileBase):
    id: int
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Experience ---

class ExperienceBase(BaseModel):
    company: str
    role: str
    period_start: Optional[str] = None
    period_end: Optional[str] = None
    location: Optional[str] = None
    tagline: Optional[str] = None
    highlights: Optional[List[str]] = []
    order: Optional[int] = 0
    is_current: Optional[bool] = False


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(ExperienceBase):
    company: Optional[str] = None
    role: Optional[str] = None


class ExperienceResponse(ExperienceBase):
    id: int

    class Config:
        from_attributes = True


# --- Education ---

class EducationBase(BaseModel):
    institution: str
    degree: str
    year: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = 0


class EducationCreate(EducationBase):
    pass


class EducationUpdate(EducationBase):
    institution: Optional[str] = None
    degree: Optional[str] = None


class EducationResponse(EducationBase):
    id: int

    class Config:
        from_attributes = True


# --- Skill ---

class SkillBase(BaseModel):
    category: str
    items: Optional[List[str]] = []
    order: Optional[int] = 0


class SkillCreate(SkillBase):
    pass


class SkillUpdate(SkillBase):
    category: Optional[str] = None


class SkillResponse(SkillBase):
    id: int

    class Config:
        from_attributes = True


# --- Certification ---

class CertificationBase(BaseModel):
    name: str
    issuer: Optional[str] = None
    year: Optional[str] = None
    badge_url: Optional[str] = None
    is_featured: Optional[bool] = False
    order: Optional[int] = 0


class CertificationCreate(CertificationBase):
    pass


class CertificationUpdate(CertificationBase):
    name: Optional[str] = None


class CertificationResponse(CertificationBase):
    id: int

    class Config:
        from_attributes = True


# --- Project ---

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    tech_stack: Optional[List[str]] = []
    period: Optional[str] = None
    category: Optional[str] = None
    company: Optional[str] = None
    role: Optional[str] = None
    highlights: Optional[List[str]] = []
    is_featured: Optional[bool] = False
    order: Optional[int] = 0


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    name: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int

    class Config:
        from_attributes = True


# --- Research ---

class ResearchBase(BaseModel):
    title: str
    description: Optional[str] = None
    type: Optional[str] = None
    focus_area: Optional[str] = None
    order: Optional[int] = 0


class ResearchCreate(ResearchBase):
    pass


class ResearchUpdate(ResearchBase):
    title: Optional[str] = None


class ResearchResponse(ResearchBase):
    id: int

    class Config:
        from_attributes = True


# --- Award ---

class AwardBase(BaseModel):
    title: str
    description: Optional[str] = None
    year: Optional[str] = None
    organization: Optional[str] = None
    order: Optional[int] = 0


class AwardCreate(AwardBase):
    pass


class AwardUpdate(AwardBase):
    title: Optional[str] = None


class AwardResponse(AwardBase):
    id: int

    class Config:
        from_attributes = True


# --- ImpactMetric ---

class ImpactMetricBase(BaseModel):
    metric: str
    label: str
    description: Optional[str] = None
    order: Optional[int] = 0


class ImpactMetricCreate(ImpactMetricBase):
    pass


class ImpactMetricUpdate(ImpactMetricBase):
    metric: Optional[str] = None
    label: Optional[str] = None


class ImpactMetricResponse(ImpactMetricBase):
    id: int

    class Config:
        from_attributes = True


# --- Auth ---

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AdminUserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True
