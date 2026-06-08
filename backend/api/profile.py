from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from backend.database.postgres import get_db
from backend.database import models, schemas

router = APIRouter(prefix="/api/v1/profile", tags=["Profile"])

@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(models.User).options(
        selectinload(models.User.skills),
        selectinload(models.User.projects),
        selectinload(models.User.experiences),
        selectinload(models.User.certifications)
    ).where(models.User.id == user_id)
    
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user

@router.post("/generate/{user_id}")
async def generate_digital_twin(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Consolidates data into the Career Digital Twin.
    """
    stmt = select(models.User).options(
        selectinload(models.User.skills),
        selectinload(models.User.projects),
        selectinload(models.User.certifications)
    ).where(models.User.id == user_id)
    
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    unique_skills = {}
    for skill in user.skills:
        skill_name = skill.name.lower()
        if skill_name not in unique_skills:
            unique_skills[skill_name] = skill

    # Merge skills from projects and certs
    for proj in user.projects:
        if proj.technologies:
            for tech in proj.technologies:
                tech_lower = tech.lower()
                if tech_lower not in unique_skills:
                    new_skill = models.Skill(user_id=user_id, name=tech, category="General")
                    db.add(new_skill)
                    unique_skills[tech_lower] = new_skill

    for cert in user.certifications:
        if cert.relevant_skills:
            for skill in cert.relevant_skills:
                skill_lower = skill.lower()
                if skill_lower not in unique_skills:
                    new_skill = models.Skill(user_id=user_id, name=skill, category=cert.domain)
                    db.add(new_skill)
                    unique_skills[skill_lower] = new_skill

    await db.commit()
    return {"message": "Digital Twin generated successfully"}

@router.get("/dashboard/stats/{user_id}")
async def get_dashboard_stats(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(models.User).options(
        selectinload(models.User.skills),
        selectinload(models.User.projects),
        selectinload(models.User.certifications),
        selectinload(models.User.experiences)
    ).where(models.User.id == user_id)
    
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return {
        "total_skills": len(user.skills),
        "total_projects": len(user.projects),
        "total_certifications": len(user.certifications),
        "total_experiences": len(user.experiences),
        "top_languages": user.top_languages,
        "github_stats": user.github_stats
    }

@router.post("/create", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

from pydantic import BaseModel
class SkillsInput(BaseModel):
    skills: str

@router.post("/{user_id}/skills")
async def add_manual_skills(user_id: int, skills_input: SkillsInput, db: AsyncSession = Depends(get_db)):
    skill_list = [s.strip() for s in skills_input.skills.split(",") if s.strip()]
    for skill_name in skill_list:
        new_skill = models.Skill(user_id=user_id, name=skill_name, category="Manual Input")
        db.add(new_skill)
    await db.commit()
    return {"message": "Skills added successfully"}
