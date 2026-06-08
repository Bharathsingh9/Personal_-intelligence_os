import datetime
from typing import Dict, Any, List

def generate_weekly_report(user: Any, current_readiness: float, missing_skills: List[Dict[str, Any]], projects: List[Dict[str, Any]]) -> Dict[str, Any]:
    top_missing = missing_skills[0]["missing_skill"] if missing_skills else "None"
    top_project = projects[0]["project_name"] if projects else "None"
    
    summary = {
        "report_date": datetime.date.today().isoformat(),
        "career_health_readiness": current_readiness,
        "fastest_growing_skill": "Agentic AI", 
        "most_important_missing_skill": top_missing,
        "best_next_project": top_project,
        "recommended_action": f"Start building a project using {top_missing}"
    }
    
    return summary
