from typing import List, Dict, Any

def run_market_etl() -> List[Dict[str, Any]]:
    trends_data = [
        {"skill_name": "Agentic AI", "target_role": "GenAI Engineer", "demand_count": 450, "weekly_growth": 230.5, "monthly_growth": 540.0},
        {"skill_name": "Graph RAG", "target_role": "GenAI Engineer", "demand_count": 320, "weekly_growth": 175.2, "monthly_growth": 310.5},
        {"skill_name": "Python", "target_role": "Data Scientist", "demand_count": 15000, "weekly_growth": 2.5, "monthly_growth": 8.0},
        {"skill_name": "LangGraph", "target_role": "AI Engineer", "demand_count": 890, "weekly_growth": 45.0, "monthly_growth": 120.0},
        {"skill_name": "MLOps", "target_role": "MLOps Engineer", "demand_count": 1200, "weekly_growth": 15.0, "monthly_growth": 35.0},
        {"skill_name": "Prompt Engineering", "target_role": "AI Engineer", "demand_count": 2100, "weekly_growth": 12.0, "monthly_growth": 25.0}
    ]
    
    return trends_data
