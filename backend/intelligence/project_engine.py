from typing import List, Dict, Any
import os
import json
from groq import Groq
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def recommend_projects(missing_skills: List[str]) -> List[Dict[str, Any]]:
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        try:
            client = Groq(api_key=api_key)
            skill_names = [s.get("missing_skill", str(s)) if isinstance(s, dict) else str(s) for s in missing_skills]
            prompt = f"""You are an expert AI Career Coach.
            The user needs to learn these core skills: {skill_names}.
            Generate 3 unique, high-impact project ideas that incorporate these skills.
            Return ONLY a valid JSON array matching this schema exactly:
            [
                {{
                    "project_name": "Project Name",
                    "technologies": ["Skill 1", "Skill 2"],
                    "covered_gaps": ["Skill 1"],
                    "scores": {{
                        "resume_impact": 85,
                        "market_demand": 90,
                        "learning_value": 95,
                        "difficulty": "Medium"
                    }},
                    "estimated_time": "3 weeks"
                }}
            ]
            Do not return any markdown wrapping, just the JSON string.
            """
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
            )
            response_content = chat_completion.choices[0].message.content.strip()
            if response_content.startswith("```json"):
                response_content = response_content[7:-3]
            elif response_content.startswith("```"):
                response_content = response_content[3:-3]
            return json.loads(response_content)
        except Exception as e:
            print(f"Groq Error: {e}")
            # Fallback to mock logic below if Groq fails
            
    all_projects = [
        {
            "name": "Graph RAG System",
            "technologies": ["LangGraph", "Vector Databases", "Python"],
            "difficulty": "Hard",
            "estimated_time": "3 weeks"
        },
        {
            "name": "Multi-Agent Research Assistant",
            "technologies": ["Agentic AI", "Python", "LLM Evaluation"],
            "difficulty": "Medium",
            "estimated_time": "2 weeks"
        },
        {
            "name": "AI Career Copilot",
            "technologies": ["FastAPI", "React", "LangChain"],
            "difficulty": "Medium",
            "estimated_time": "4 weeks"
        }
    ]
    
    recommendations = []
    for proj in all_projects:
        covered_gaps = [tech for tech in proj["technologies"] if tech in missing_skills]
        resume_impact = len(covered_gaps) * 15 
        recommendations.append({
            "project_name": proj["name"],
            "technologies": proj["technologies"],
            "covered_gaps": covered_gaps,
            "scores": {
                "resume_impact": min(100, resume_impact + 40),
                "market_demand": 85,
                "learning_value": 90,
                "difficulty": proj["difficulty"]
            },
            "estimated_time": proj["estimated_time"]
        })
    recommendations.sort(key=lambda x: x["scores"]["resume_impact"], reverse=True)
    return recommendations
