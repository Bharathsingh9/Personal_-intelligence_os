from fastapi import APIRouter
from backend.intelligence.reporter import generate_weekly_report

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])

@router.get("/latest/{user_id}")
async def get_latest_report(user_id: int):
    missing = [{"missing_skill": "LangGraph"}]
    projects = [{"project_name": "Graph RAG System"}]
    return generate_weekly_report(None, 67.0, missing, projects)
