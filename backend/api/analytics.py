from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Any
from backend.database.postgres import get_db
from backend.database import models, schemas
from backend.analytics.readiness_score import compute_readiness_matrix
from backend.analytics.skill_gap_analysis import analyze_skill_gap

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])

@router.get("/roles", response_model=List[schemas.RoleResponse])
async def get_roles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Role).options(selectinload(models.Role.role_skills)))
    return result.scalars().all()

@router.post("/readiness/{user_id}")
async def compute_readiness(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(models.User).options(
        selectinload(models.User.skills),
        selectinload(models.User.projects),
        selectinload(models.User.experiences),
        selectinload(models.User.certifications)
    ).where(models.User.id == user_id)
    user_result = await db.execute(stmt)
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    roles_result = await db.execute(select(models.Role).options(selectinload(models.Role.role_skills)))
    roles = roles_result.scalars().all()
    
    readiness_results = compute_readiness_matrix(user, roles)
    
    for res in readiness_results:
        await db.execute(
            models.ReadinessScore.__table__.delete().where(
                (models.ReadinessScore.user_id == user_id) & 
                (models.ReadinessScore.role_id == res["role_id"])
            )
        )
        db_score = models.ReadinessScore(
            user_id=user_id,
            role_id=res["role_id"],
            total_score=res["total_score"],
            breakdown=res["breakdown"]
        )
        db.add(db_score)
        
    await db.commit()
    return {"user_id": user_id, "readiness_scores": readiness_results}

@router.get("/skill-gap/{user_id}/{role_id}")
async def get_skill_gap(user_id: int, role_id: int, db: AsyncSession = Depends(get_db)):
    user_result = await db.execute(select(models.User).options(selectinload(models.User.skills)).where(models.User.id == user_id))
    user = user_result.scalar_one_or_none()
    
    role_result = await db.execute(select(models.Role).options(selectinload(models.Role.role_skills)).where(models.Role.id == role_id))
    role = role_result.scalar_one_or_none()
    
    if not user or not role:
        raise HTTPException(status_code=404, detail="User or Role not found")
        
    score_result = await db.execute(
        select(models.ReadinessScore)
        .where((models.ReadinessScore.user_id == user_id) & (models.ReadinessScore.role_id == role_id))
    )
    score_record = score_result.scalar_one_or_none()
    current_score = score_record.total_score if score_record else 0.0
    
    gaps = analyze_skill_gap(user, role, current_score)
    
    await db.execute(
        models.SkillGap.__table__.delete().where(
            (models.SkillGap.user_id == user_id) & 
            (models.SkillGap.role_id == role_id)
        )
    )
    for gap in gaps:
        db_gap = models.SkillGap(
            user_id=user_id,
            role_id=role_id,
            missing_skill=gap["skill_name"],
            impact_score=gap["impact_score"],
            recommended_order=gap["recommended_order"]
        )
        db.add(db_gap)
        
    await db.commit()
    
    return {
        "user_id": user_id,
        "role_id": role_id,
        "role_name": role.name,
        "current_score": current_score,
        "missing_skills": gaps
    }
