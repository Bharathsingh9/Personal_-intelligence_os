from typing import Dict, Any

def analyze_leetcode_profile(username: str) -> Dict[str, Any]:
    difficulty_dist = {
        "Easy": 120,
        "Medium": 180,
        "Hard": 35
    }
    
    topic_mastery = {
        "Strong": ["Arrays", "Dynamic Programming", "Sliding Window"],
        "Moderate": ["Trees", "Binary Search"],
        "Weak": ["Graphs", "Segment Trees"]
    }
    
    base_score = (difficulty_dist["Easy"] * 0.5) + (difficulty_dist["Medium"] * 1.5) + (difficulty_dist["Hard"] * 3.0)
    readiness_score = min(100.0, base_score / 5.0) 
    
    dsa_strength = "Advanced" if readiness_score > 80 else "Intermediate" if readiness_score > 50 else "Beginner"
    
    return {
        "leetcode_username": username,
        "readiness_score": round(readiness_score, 2),
        "dsa_strength_level": dsa_strength,
        "difficulty_distribution": difficulty_dist,
        "topic_mastery": topic_mastery
    }
