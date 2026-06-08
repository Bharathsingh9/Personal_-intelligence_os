from typing import Dict, Any, List
import math

def analyze_github_deep(repos_data: List[Dict[str, Any]], user_data: Dict[str, Any]) -> Dict[str, Any]:
    detected_tech = set()
    strengths = set()
    improvement_areas = {"Docker", "CI/CD", "Cloud Deployment"}
    
    total_commits_estimate = 0
    language_counts = {}
    repo_quality_score = 0.0
    
    for repo in repos_data:
        lang = repo.get("language")
        if lang:
            language_counts[lang] = language_counts.get(lang, 0) + 1
            detected_tech.add(lang)
            
        name = (repo.get("name") or "").lower()
        if "react" in name or "ui" in name:
            detected_tech.add("React")
        if "api" in name or "backend" in name:
            detected_tech.add("FastAPI")
        if "data" in name or "ml" in name:
            detected_tech.add("Machine Learning")
            
        # Add basic commit estimate per repo for now, or use real data if available
        total_commits_estimate += repo.get("size", 50) 
        
        # Calculate Repo Quality
        stars = repo.get("stargazers_count", 0)
        repo_quality_score += stars * 2
            
    if "Python" in language_counts and language_counts["Python"] > 1:
        strengths.add("Python")
    if "TypeScript" in language_counts or "JavaScript" in language_counts:
        strengths.add("Frontend Development")
    if "Machine Learning" in detected_tech:
        strengths.add("Machine Learning")
        
    # C: Total Commits (Max 40 points, log scaled: min(40, log10(commits) * 15))
    commits_val = max(1, total_commits_estimate)
    c_score = min(40.0, math.log10(commits_val) * 15.0)
    
    # L: Languages Mastered (Max 20 points, min(20, num_languages * 4))
    l_score = min(20.0, len(detected_tech) * 4.0)
    
    # R: Repo Quality (Max 40 points, avg repo stars + base points)
    # Give a base score of 10 if there are any repos, plus stars
    r_base = 10.0 if repos_data else 0.0
    r_score = min(40.0, r_base + repo_quality_score)
    
    dev_score = c_score + l_score + r_score
    
    return {
        "developer_score": round(dev_score, 2),
        "tech_stack_detected": list(detected_tech),
        "strengths": list(strengths) if strengths else ["Backend Development"],
        "improvement_areas": list(improvement_areas),
        "activity_metrics": {
            "total_repos": len(repos_data),
            "estimated_commits": total_commits_estimate,
            "followers": user_data.get("followers", 0)
        }
    }
