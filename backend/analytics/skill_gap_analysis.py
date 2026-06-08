from typing import List, Dict, Any
from backend.database import models

def analyze_skill_gap(user: models.User, role: models.Role, current_score: float) -> List[Dict[str, Any]]:
    """
    Analyzes missing skills and simulates the impact of acquiring them.
    """
    user_skills = {skill.name.lower() for skill in user.skills}
    role_skills_list = role.role_skills
    
    missing_skills = []
    
    for rs in role_skills_list:
        if rs.skill_name.lower() not in user_skills:
            missing_skills.append(rs)
            
    if not missing_skills:
        return []
        
    gaps = []
    
    max_skill_score = 0.0
    for r in role_skills_list:
        max_skill_score += (r.weight * 2.0 if r.is_core else r.weight)
        
    if max_skill_score == 0:
        return []
        
    for ms in missing_skills:
        weight_impact = (ms.weight * 2.0 if ms.is_core else ms.weight)
        
        simulated_impact = 0.45 * (weight_impact / max_skill_score)
        
        if ms.is_core:
            simulated_impact += 0.10
            
        gaps.append({
            "skill_name": ms.skill_name,
            "impact_score": round(simulated_impact * 100, 2),
            "is_core": ms.is_core
        })
        
    gaps.sort(key=lambda x: x["impact_score"], reverse=True)
    
    for idx, gap in enumerate(gaps):
        gap["recommended_order"] = idx + 1
        
    return gaps
