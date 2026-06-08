from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from backend.database.postgres import get_db
from backend.database import models, schemas
from backend.intelligence.market_etl import run_market_etl
import datetime

router = APIRouter(prefix="/api/v1/market", tags=["Market Intelligence"])

@router.post("/etl/run")
async def trigger_etl(db: AsyncSession = Depends(get_db)):
    trends = run_market_etl()
    
    await db.execute(models.SkillDemandTrend.__table__.delete())
    
    for t in trends:
        db.add(models.SkillDemandTrend(
            skill_name=t["skill_name"],
            target_role=t["target_role"],
            demand_count=t["demand_count"],
            weekly_growth=t["weekly_growth"],
            monthly_growth=t["monthly_growth"],
            record_date=datetime.date.today()
        ))
        
    await db.commit()
    return {"message": "Market ETL triggered successfully"}

@router.get("/trends", response_model=List[schemas.SkillDemandTrendResponse])
async def get_trends(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.SkillDemandTrend).order_by(models.SkillDemandTrend.weekly_growth.desc()))
    return result.scalars().all()
