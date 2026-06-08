from typing import List, Dict, Any

def analyze_skill_gaps(
    user_skills: List[str], 
    role_requirements: List[Dict[str, Any]], 
    market_frequencies: Dict[str, float] = None
) -> List[Dict[str, Any]]:
    """
    Identifies missing skills and calculates gap severity.
    Impact Score = (Skill Frequency in Job Market * 0.6) + (Is_Core_Multiplier * 0.4)
    Where Is_Core_Multiplier = 10 if core else 3.
    """
    if market_frequencies is None:
        market_frequencies = {}

    user_skills_lower = set([s.lower() for s in user_skills])
    
    missing_skills = []
    
    for req in role_requirements:
        skill_name = req['skill_name']
        if skill_name.lower() not in user_skills_lower:
            is_core = req.get('is_core', False)
            
            # Base variables
            market_freq = market_frequencies.get(skill_name, 5.0) # default to mid-range out of 10
            core_multiplier = 10.0 if is_core else 3.0
            
            impact_score = (market_freq * 0.6) + (core_multiplier * 0.4)
            
            missing_skills.append({
                "missing_skill": skill_name,
                "is_core": is_core,
                "impact_score": round(impact_score, 1)
            })
            
    # Sort by highest impact score first
    missing_skills.sort(key=lambda x: x['impact_score'], reverse=True)
    
    # Add recommended order
    for idx, skill in enumerate(missing_skills):
        skill['recommended_order'] = idx + 1
        
    return missing_skills
