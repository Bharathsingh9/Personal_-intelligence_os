from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict, Any, List
from pydantic import BaseModel
from backend.database.postgres import get_db
from backend.database import models
from backend.intelligence.roadmap_generator import generate_roadmap
from backend.intelligence.project_engine import recommend_projects

router = APIRouter(prefix="/api/v1/copilot", tags=["Copilot Multi-Agent"])

class ChatRequest(BaseModel):
    user_id: int
    query: str

class ChatResponse(BaseModel):
    response_text: str
    roadmap: Dict[str, Any] = None
    projects: List[Dict[str, Any]] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_with_copilot(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    query = request.query.lower()
    
    user_result = await db.execute(select(models.User).where(models.User.id == request.user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    missing_skills_mock = [
        {"missing_skill": "LangGraph", "impact_score": 8.4},
        {"missing_skill": "Vector Databases", "impact_score": 6.2},
        {"missing_skill": "LLM Evaluation", "impact_score": 5.1}
    ]
    missing_skill_names = [s["missing_skill"] for s in missing_skills_mock]
    
    response = ChatResponse(response_text="I can help with that! Here is my analysis.")
    
    if "roadmap" in query or "how do i become" in query or "learn" in query:
        roadmap = generate_roadmap("GenAI Engineer", missing_skills_mock, [])
        response.roadmap = roadmap
        response.response_text = "I've generated a personalized 30-day learning roadmap focusing on LangGraph and Vector Databases."
        
    if "project" in query or "build" in query:
        projects = recommend_projects(missing_skill_names)
        response.projects = projects
        if response.roadmap:
            response.response_text += " I also found some great projects you can build to apply these skills."
        else:
            response.response_text = "Here are the top project recommendations tailored to close your skill gaps."
            
    if not response.roadmap and not response.projects:
        response.response_text = "I am your Career Copilot. I can generate learning roadmaps or recommend high-impact projects based on your profile gaps. What would you like to explore?"
        
    return response
