from fastapi import APIRouter, UploadFile, File, Depends, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.postgres import get_db
from backend.ingestion.resume_parser import parse_resume
from backend.ingestion.github_parser import analyze_github_profile
from backend.ingestion.certificate_parser import parse_certification
from backend.database import models, schemas
import json

router = APIRouter(prefix="/api/v1/ingest", tags=["Ingestion"])

@router.post("/resume")
async def ingest_resume(
    user_id: int = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
    content = await file.read()
    parsed_data = parse_resume(content)
    
    # Normally we would save this raw data or start inserting into DB.
    # For Phase 1, we will save the extracted skills directly.
    for skill in parsed_data.get("skills", []):
        db_skill = models.Skill(user_id=user_id, name=skill["name"], category=skill["category"])
        db.add(db_skill)
        
    await db.commit()
    
    return {"message": "Resume ingested successfully", "extracted_data": parsed_data}

@router.post("/github")
async def ingest_github(
    user_id: int,
    username: str,
    token: str = None,
    db: AsyncSession = Depends(get_db)
):
    github_data = await analyze_github_profile(username, token)
    if "error" in github_data:
        raise HTTPException(status_code=400, detail=github_data["error"])
        
    user = await db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.github_username = username
    user.github_stats = github_data["github_stats"]
    user.top_languages = github_data["top_languages"]
    
    # Save projects
    for proj in github_data.get("projects", []):
        db_project = models.Project(
            user_id=user_id,
            name=proj["name"],
            description=proj["description"],
            technologies=proj["technologies"],
            source="GitHub"
        )
        db.add(db_project)
        
    await db.commit()
    return {"message": "GitHub profile ingested successfully", "stats": github_data["github_stats"]}

@router.post("/certification")
async def ingest_certification(
    user_id: int,
    cert_data: dict,
    db: AsyncSession = Depends(get_db)
):
    parsed_cert = parse_certification(cert_data)
    
    db_cert = models.Certification(
        user_id=user_id,
        name=parsed_cert["name"],
        issuer=parsed_cert["issuer"],
        domain=parsed_cert["domain"],
        relevant_skills=parsed_cert["relevant_skills"]
    )
    db.add(db_cert)
    await db.commit()
    
    return {"message": "Certification ingested successfully"}
