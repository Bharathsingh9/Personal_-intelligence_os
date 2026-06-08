from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any
from backend.database.postgres import get_db
from backend.database import models, schemas
import os
import requests
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
from backend.intelligence.github_deep_scanner import analyze_github_deep
from backend.intelligence.leetcode_client import analyze_leetcode_profile
from backend.intelligence.readiness_engine import calculate_readiness
from backend.intelligence.skill_gap_engine import analyze_skill_gaps
from typing import List

router = APIRouter(prefix="/api/v1/intelligence", tags=["Intelligence"])

@router.post("/readiness/{user_id}", response_model=List[schemas.ReadinessScoreResponse])
async def calculate_user_readiness(user_id: int, db: AsyncSession = Depends(get_db)):
    user_res = await db.execute(select(models.User).where(models.User.id == user_id))
    user = user_res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    skills_res = await db.execute(select(models.Skill).where(models.Skill.user_id == user_id))
    user_skills = [s.name for s in skills_res.scalars().all()]
    
    roles_res = await db.execute(select(models.Role))
    roles = roles_res.scalars().all()
    
    await db.execute(models.ReadinessScore.__table__.delete().where(models.ReadinessScore.user_id == user_id))
    
    results = []
    for role in roles:
        role_skills_res = await db.execute(select(models.RoleSkill).where(models.RoleSkill.role_id == role.id))
        reqs = [{"skill_name": rs.skill_name, "is_core": rs.is_core, "weight": rs.weight} for rs in role_skills_res.scalars().all()]
        
        score_data = calculate_readiness(user_skills, reqs, years_of_experience=3.0, project_complexity_score=5.0)
        
        db_score = models.ReadinessScore(
            user_id=user_id,
            role_id=role.id,
            total_score=score_data["total_score"],
            breakdown=score_data["breakdown"]
        )
        db.add(db_score)
        results.append(db_score)
        
    await db.commit()
    for r in results:
        await db.refresh(r)
    return results

@router.get("/skill-gaps/{user_id}", response_model=List[schemas.SkillGapResponse])
async def get_user_skill_gaps(user_id: int, role_id: int, db: AsyncSession = Depends(get_db)):
    skills_res = await db.execute(select(models.Skill).where(models.Skill.user_id == user_id))
    user_skills = [s.name for s in skills_res.scalars().all()]
    
    role_skills_res = await db.execute(select(models.RoleSkill).where(models.RoleSkill.role_id == role_id))
    reqs = [{"skill_name": rs.skill_name, "is_core": rs.is_core} for rs in role_skills_res.scalars().all()]
    
    gaps = analyze_skill_gaps(user_skills, reqs)
    
    await db.execute(models.SkillGap.__table__.delete().where(models.SkillGap.user_id == user_id).where(models.SkillGap.role_id == role_id))
    
    results = []
    for gap in gaps:
        db_gap = models.SkillGap(
            user_id=user_id,
            role_id=role_id,
            missing_skill=gap["missing_skill"],
            impact_score=gap["impact_score"],
            recommended_order=gap["recommended_order"]
        )
        db.add(db_gap)
        results.append(db_gap)
        
    await db.commit()
    for r in results:
        await db.refresh(r)
    return results

@router.post("/github/{user_id}", response_model=schemas.GitHubAnalyticsResponse)
async def analyze_github(user_id: int, db: AsyncSession = Depends(get_db)):
    user_result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    github_username = user.github_username or ""
    github_token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {github_token}"} if github_token else {}
    
    user_resp = requests.get(f"https://api.github.com/users/{github_username}", headers=headers)
    user_data = user_resp.json() if user_resp.status_code == 200 else {"followers": 0}
    
    repos_resp = requests.get(f"https://api.github.com/users/{github_username}/repos?per_page=100", headers=headers)
    repos_data = repos_resp.json() if repos_resp.status_code == 200 else []
    
    if not isinstance(repos_data, list):
        repos_data = []
    
    analytics = analyze_github_deep(repos_data, user_data)
    
    await db.execute(models.GitHubAnalytics.__table__.delete().where(models.GitHubAnalytics.user_id == user_id))
    
    db_analytics = models.GitHubAnalytics(
        user_id=user_id,
        developer_score=analytics["developer_score"],
        tech_stack_detected=analytics["tech_stack_detected"],
        strengths=analytics["strengths"],
        improvement_areas=analytics["improvement_areas"],
        activity_metrics=analytics["activity_metrics"]
    )
    db.add(db_analytics)
    await db.commit()
    await db.refresh(db_analytics)
    
    return db_analytics

@router.post("/leetcode/{user_id}", response_model=schemas.LeetCodeAnalyticsResponse)
async def analyze_leetcode(user_id: int, db: AsyncSession = Depends(get_db)):
    user_result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    analytics = analyze_leetcode_profile(user.github_username or "default")
    
    await db.execute(models.LeetCodeAnalytics.__table__.delete().where(models.LeetCodeAnalytics.user_id == user_id))
    
    db_analytics = models.LeetCodeAnalytics(
        user_id=user_id,
        leetcode_username=analytics["leetcode_username"],
        readiness_score=analytics["readiness_score"],
        dsa_strength_level=analytics["dsa_strength_level"],
        difficulty_distribution=analytics["difficulty_distribution"],
        topic_mastery=analytics["topic_mastery"]
    )
    db.add(db_analytics)
    await db.commit()
    await db.refresh(db_analytics)
    
    return db_analytics
