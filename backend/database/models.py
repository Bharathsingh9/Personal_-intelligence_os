from sqlalchemy import Column, Integer, String, Date, JSON, ForeignKey, Text, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from backend.database.postgres import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    github_username = Column(String, unique=True, index=True, nullable=True)
    github_stats = Column(JSON, nullable=True)
    top_languages = Column(JSON, nullable=True)

    skills = relationship("Skill", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    experiences = relationship("Experience", back_populates="user", cascade="all, delete-orphan")
    certifications = relationship("Certification", back_populates="user", cascade="all, delete-orphan")
    
    readiness_scores = relationship("ReadinessScore", back_populates="user", cascade="all, delete-orphan")
    skill_gaps = relationship("SkillGap", back_populates="user", cascade="all, delete-orphan")
    github_analytics = relationship("GitHubAnalytics", back_populates="user", uselist=False, cascade="all, delete-orphan")
    leetcode_analytics = relationship("LeetCodeAnalytics", back_populates="user", uselist=False, cascade="all, delete-orphan")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    category = Column(String, nullable=True)

    user = relationship("User", back_populates="skills")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    technologies = Column(JSON, nullable=True)
    source = Column(String, nullable=True)

    user = relationship("User", back_populates="projects")

class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    company = Column(String)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    description = Column(Text, nullable=True)

    user = relationship("User", back_populates="experiences")

class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    issuer = Column(String, nullable=True)
    domain = Column(String, nullable=True)
    relevant_skills = Column(JSON, nullable=True)

    user = relationship("User", back_populates="certifications")

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(String, nullable=True)
    min_experience_years = Column(Integer, default=0)

    role_skills = relationship("RoleSkill", back_populates="role", cascade="all, delete-orphan")
    readiness_scores = relationship("ReadinessScore", back_populates="role", cascade="all, delete-orphan")
    skill_gaps = relationship("SkillGap", back_populates="role", cascade="all, delete-orphan")

class RoleSkill(Base):
    __tablename__ = "role_skills"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    skill_name = Column(String, index=True)
    weight = Column(Float, default=1.0)
    is_core = Column(Boolean, default=False)

    role = relationship("Role", back_populates="role_skills")

class ReadinessScore(Base):
    __tablename__ = "readiness_scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    total_score = Column(Float, default=0.0)
    breakdown = Column(JSON, nullable=True)

    user = relationship("User", back_populates="readiness_scores")
    role = relationship("Role", back_populates="readiness_scores")

class SkillGap(Base):
    __tablename__ = "skill_gaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    missing_skill = Column(String)
    impact_score = Column(Float, default=0.0)
    recommended_order = Column(Integer, default=0)

    user = relationship("User", back_populates="skill_gaps")
    role = relationship("Role", back_populates="skill_gaps")

class GitHubAnalytics(Base):
    __tablename__ = "github_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    developer_score = Column(Float, default=0.0)
    tech_stack_detected = Column(JSON, nullable=True)
    strengths = Column(JSON, nullable=True)
    improvement_areas = Column(JSON, nullable=True)
    activity_metrics = Column(JSON, nullable=True)
    
    user = relationship("User", back_populates="github_analytics")

class LeetCodeAnalytics(Base):
    __tablename__ = "leetcode_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    leetcode_username = Column(String, nullable=True)
    readiness_score = Column(Float, default=0.0)
    dsa_strength_level = Column(String, nullable=True)
    difficulty_distribution = Column(JSON, nullable=True)
    topic_mastery = Column(JSON, nullable=True)
    
    user = relationship("User", back_populates="leetcode_analytics")

class JobListing(Base):
    __tablename__ = "job_listings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String)
    location = Column(String, nullable=True)
    required_skills = Column(JSON, nullable=True)
    posted_at = Column(DateTime, default=datetime.datetime.utcnow)

class SkillDemandTrend(Base):
    __tablename__ = "skill_demand_trends"
    
    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String, index=True)
    target_role = Column(String, index=True, nullable=True)
    demand_count = Column(Integer, default=0)
    weekly_growth = Column(Float, default=0.0)
    monthly_growth = Column(Float, default=0.0)
    record_date = Column(Date, default=datetime.date.today)

class LearningRoadmap(Base):
    __tablename__ = "learning_roadmaps"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    target_role = Column(String, index=True)
    roadmap_json = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ProjectRecommendation(Base):
    __tablename__ = "project_recommendations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    target_role = Column(String, index=True)
    projects_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class CareerSimulation(Base):
    __tablename__ = "career_simulations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    scenario_name = Column(String)
    current_score = Column(Float)
    predicted_score = Column(Float)
    deltas_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class WeeklyReport(Base):
    __tablename__ = "weekly_reports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    report_date = Column(Date, default=datetime.date.today)
    s3_pdf_url = Column(String, nullable=True)
    summary_json = Column(JSON)
