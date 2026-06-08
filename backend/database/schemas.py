from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date

# Skill Schemas
class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillResponse(SkillBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

# Project Schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    technologies: Optional[List[str]] = None
    source: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

# Experience Schemas
class ExperienceBase(BaseModel):
    title: str
    company: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceResponse(ExperienceBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

# Certification Schemas
class CertificationBase(BaseModel):
    name: str
    issuer: Optional[str] = None
    domain: Optional[str] = None
    relevant_skills: Optional[List[str]] = None

class CertificationCreate(CertificationBase):
    pass

class CertificationResponse(CertificationBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    name: str
    email: Optional[str] = None
    github_username: Optional[str] = None
    github_stats: Optional[Dict[str, Any]] = None
    top_languages: Optional[Dict[str, Any]] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    skills: List[SkillResponse] = []
    projects: List[ProjectResponse] = []
    experiences: List[ExperienceResponse] = []
    certifications: List[CertificationResponse] = []
    
    class Config:
        from_attributes = True

# RoleSkill Schemas
class RoleSkillBase(BaseModel):
    skill_name: str
    weight: float = 1.0
    is_core: bool = False

class RoleSkillResponse(RoleSkillBase):
    id: int
    role_id: int
    class Config:
        from_attributes = True

# Role Schemas
class RoleBase(BaseModel):
    name: str
    category: Optional[str] = None
    min_experience_years: int = 0

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int
    role_skills: List[RoleSkillResponse] = []
    class Config:
        from_attributes = True

# ReadinessScore Schemas
class ReadinessScoreBase(BaseModel):
    total_score: float
    breakdown: Optional[Dict[str, Any]] = None

class ReadinessScoreResponse(ReadinessScoreBase):
    id: int
    user_id: int
    role_id: int
    class Config:
        from_attributes = True

# SkillGap Schemas
class SkillGapBase(BaseModel):
    missing_skill: str
    impact_score: float
    recommended_order: int

class SkillGapResponse(SkillGapBase):
    id: int
    user_id: int
    role_id: int
    class Config:
        from_attributes = True

# New Schemas for Phase 4, 5, 6
class GitHubAnalyticsBase(BaseModel):
    developer_score: float
    tech_stack_detected: Optional[List[str]] = None
    strengths: Optional[List[str]] = None
    improvement_areas: Optional[List[str]] = None
    activity_metrics: Optional[Dict[str, Any]] = None

class GitHubAnalyticsResponse(GitHubAnalyticsBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class LeetCodeAnalyticsBase(BaseModel):
    leetcode_username: Optional[str] = None
    readiness_score: float
    dsa_strength_level: Optional[str] = None
    difficulty_distribution: Optional[Dict[str, int]] = None
    topic_mastery: Optional[Dict[str, Any]] = None

class LeetCodeAnalyticsResponse(LeetCodeAnalyticsBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class JobListingBase(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    required_skills: Optional[List[str]] = None

class JobListingResponse(JobListingBase):
    id: int
    posted_at: date
    class Config:
        from_attributes = True

class SkillDemandTrendBase(BaseModel):
    skill_name: str
    target_role: Optional[str] = None
    demand_count: int
    weekly_growth: float
    monthly_growth: float

class SkillDemandTrendResponse(SkillDemandTrendBase):
    id: int
    record_date: date
    class Config:
        from_attributes = True

# New Schemas for Phase 7-12
class LearningRoadmapBase(BaseModel):
    target_role: str
    roadmap_json: Dict[str, Any]
    is_active: bool = True

class LearningRoadmapResponse(LearningRoadmapBase):
    id: int
    user_id: int
    created_at: Any
    class Config:
        from_attributes = True

class ProjectRecommendationBase(BaseModel):
    target_role: str
    projects_json: List[Dict[str, Any]]

class ProjectRecommendationResponse(ProjectRecommendationBase):
    id: int
    user_id: int
    created_at: Any
    class Config:
        from_attributes = True

class CareerSimulationBase(BaseModel):
    scenario_name: str
    current_score: float
    predicted_score: float
    deltas_json: Dict[str, Any]

class CareerSimulationResponse(CareerSimulationBase):
    id: int
    user_id: int
    created_at: Any
    class Config:
        from_attributes = True

class WeeklyReportBase(BaseModel):
    s3_pdf_url: Optional[str] = None
    summary_json: Dict[str, Any]

class WeeklyReportResponse(WeeklyReportBase):
    id: int
    user_id: int
    report_date: date
    class Config:
        from_attributes = True
