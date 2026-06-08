import pandas as pd
import numpy as np
from typing import List, Dict, Any
from backend.database import models

def compute_readiness_matrix(user: models.User, roles: List[models.Role]) -> List[Dict[str, Any]]:
    """
    Computes the readiness score matrix for a user against a list of roles.
    """
    user_skills = {skill.name.lower() for skill in user.skills}
    user_projects_tech = {tech.lower() for proj in user.projects for tech in (proj.technologies or [])}
    user_certs_domain = {cert.domain.lower() for cert in user.certifications if cert.domain}
    
    total_exp_years = 0
    for exp in user.experiences:
        if exp.start_date and exp.end_date:
            days = (exp.end_date - exp.start_date).days
            total_exp_years += days / 365.25
            
    results = []
    
    for role in roles:
        role_skills_list = role.role_skills
        if not role_skills_list:
            continue
            
        skill_score = 0.0
        max_skill_score = 0.0
        core_miss_penalty = 0.0
        
        for rs in role_skills_list:
            weight = rs.weight
            if rs.is_core:
                weight *= 2.0
                
            max_skill_score += weight
            
            if rs.skill_name.lower() in user_skills:
                skill_score += weight
            elif rs.is_core:
                core_miss_penalty += 0.10
                
        normalized_skill_score = (skill_score / max_skill_score) if max_skill_score > 0 else 0.0
        
        proj_score = 0.0
        role_skill_names = {rs.skill_name.lower() for rs in role_skills_list}
        matching_tech = user_projects_tech.intersection(role_skill_names)
        
        if len(matching_tech) > 0:
            proj_score = min(1.0, len(matching_tech) / max(3, len(role_skill_names)*0.5))
            
        exp_score = 0.0
        if role.min_experience_years > 0:
            exp_score = min(1.0, total_exp_years / role.min_experience_years)
        else:
            exp_score = 1.0
            
        cert_score = 0.0
        if role.category and role.category.lower() in user_certs_domain:
            cert_score = 1.0
            
        total_score = (
            (0.45 * normalized_skill_score) + 
            (0.25 * proj_score) + 
            (0.20 * exp_score) + 
            (0.10 * cert_score)
        )
        
        total_score -= core_miss_penalty
        total_score = max(0.0, min(1.0, total_score))
        
        results.append({
            "role_id": role.id,
            "role_name": role.name,
            "total_score": round(total_score * 100, 2),
            "breakdown": {
                "skills_match": round(normalized_skill_score * 100, 2),
                "projects_match": round(proj_score * 100, 2),
                "experience_match": round(exp_score * 100, 2),
                "certifications_match": round(cert_score * 100, 2)
            }
        })
        
    return results
