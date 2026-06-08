from typing import Dict, Any, List

def run_simulation(current_score: float, hypothetical_skills: List[str], target_role: str) -> Dict[str, Any]:
    impact = len(hypothetical_skills) * 4.5 
    predicted_score = min(100.0, current_score + impact)
    
    return {
        "scenario_name": f"Learn {', '.join(hypothetical_skills)}",
        "target_role": target_role,
        "current_score": current_score,
        "predicted_score": predicted_score,
        "expected_increase": round(predicted_score - current_score, 2),
        "confidence_score": 85.0
    }
