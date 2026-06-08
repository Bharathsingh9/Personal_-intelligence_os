from typing import List, Dict, Any

def calculate_readiness(
    user_skills: List[str], 
    role_requirements: List[Dict[str, Any]], 
    years_of_experience: float, 
    project_complexity_score: float
) -> Dict[str, Any]:
    """
    Calculates the career readiness score for a specific role based on the algorithm:
    Readiness Score = (Core Skill Match * 0.5) + (Secondary Skill Match * 0.2) + (Experience Weight * 0.15) + (Project Complexity * 0.15)
    """
    user_skills_lower = set([s.lower() for s in user_skills])
    
    core_reqs = [r for r in role_requirements if r.get('is_core', False)]
    sec_reqs = [r for r in role_requirements if not r.get('is_core', False)]
    
    # Core Skill Match
    core_score = 0.0
    missing_core = 0
    if core_reqs:
        for req in core_reqs:
            if req['skill_name'].lower() in user_skills_lower:
                core_score += req.get('weight', 1.0)
            else:
                missing_core += 1
                
        max_core_score = sum(r.get('weight', 1.0) for r in core_reqs)
        core_match_percent = core_score / max_core_score if max_core_score > 0 else 0
        # Penalty: -10% per missing core skill
        core_match_percent = max(0.0, core_match_percent - (missing_core * 0.10))
    else:
        core_match_percent = 1.0
        
    # Secondary Skill Match
    sec_score = 0.0
    if sec_reqs:
        for req in sec_reqs:
            if req['skill_name'].lower() in user_skills_lower:
                sec_score += req.get('weight', 1.0)
        
        max_sec_score = sum(r.get('weight', 1.0) for r in sec_reqs)
        sec_match_percent = sec_score / max_sec_score if max_sec_score > 0 else 0
    else:
        sec_match_percent = 1.0
        
    # Experience Weight (Assuming 5 years is max needed for 100% in this mock, could be dynamic per role)
    target_experience = 5.0
    exp_percent = min(1.0, years_of_experience / target_experience)
    
    # Project Complexity (Assuming max score is 10)
    proj_percent = min(1.0, project_complexity_score / 10.0)
    
    # Final Score Calculation
    total_score = (core_match_percent * 0.5) + (sec_match_percent * 0.2) + (exp_percent * 0.15) + (proj_percent * 0.15)
    total_score_percentage = round(total_score * 100, 1)
    
    breakdown = {
        "core_match_percent": round(core_match_percent * 100, 1),
        "secondary_match_percent": round(sec_match_percent * 100, 1),
        "experience_percent": round(exp_percent * 100, 1),
        "project_percent": round(proj_percent * 100, 1),
        "missing_core_skills_count": missing_core
    }
    
    return {
        "total_score": total_score_percentage,
        "breakdown": breakdown
    }
