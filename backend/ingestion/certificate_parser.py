from typing import Dict, Any

def parse_certification(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Standardize incoming certification data.
    """
    return {
        "name": data.get("name"),
        "issuer": data.get("issuer"),
        "domain": data.get("domain", "General"),
        "relevant_skills": data.get("relevant_skills", [])
    }
