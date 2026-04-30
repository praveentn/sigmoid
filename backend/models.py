from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.types import JSON
from backend.database import Base


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    title = Column(String)
    company = Column(String)
    tagline = Column(Text)
    bio = Column(Text)
    email = Column(String)
    phone = Column(String)
    location = Column(String)
    linkedin_url = Column(String)
    credly_url = Column(String)
    visa_info = Column(String)
    years_experience = Column(Integer)
    solutions_delivered = Column(Integer)
    photo_url = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Experience(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    period_start = Column(String)
    period_end = Column(String)
    location = Column(String)
    tagline = Column(Text)
    highlights = Column(JSON, default=list)
    order = Column(Integer, default=0)
    is_current = Column(Boolean, default=False)


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True)
    institution = Column(String, nullable=False)
    degree = Column(String, nullable=False)
    year = Column(String)
    description = Column(Text)
    order = Column(Integer, default=0)


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    items = Column(JSON, default=list)
    order = Column(Integer, default=0)


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    issuer = Column(String)
    year = Column(String)
    badge_url = Column(String)
    is_featured = Column(Boolean, default=False)
    order = Column(Integer, default=0)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    tech_stack = Column(JSON, default=list)
    period = Column(String)
    category = Column(String)
    company = Column(String)
    role = Column(String)
    highlights = Column(JSON, default=list)
    is_featured = Column(Boolean, default=False)
    order = Column(Integer, default=0)


class Research(Base):
    __tablename__ = "research"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    type = Column(String)
    focus_area = Column(String)
    order = Column(Integer, default=0)


class Award(Base):
    __tablename__ = "awards"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    year = Column(String)
    organization = Column(String)
    order = Column(Integer, default=0)


class ImpactMetric(Base):
    __tablename__ = "impact_metrics"

    id = Column(Integer, primary_key=True)
    metric = Column(String, nullable=False)
    label = Column(String, nullable=False)
    description = Column(Text)
    order = Column(Integer, default=0)


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
