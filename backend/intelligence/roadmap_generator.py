from typing import List, Dict, Any
import os
import json
from groq import Groq
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def generate_roadmap(target_role: str, missing_skills: List[Dict[str, Any]], market_trends: List[Dict[str, Any]]) -> Dict[str, Any]:
    roadmap = {
        "target_role": target_role,
        "duration_weeks": 4,
        "weeks": []
    }
    
    if not missing_skills:
        return roadmap

    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        try:
            client = Groq(api_key=api_key)
            skill_names = [s.get("missing_skill", str(s)) if isinstance(s, dict) else str(s) for s in missing_skills]
            prompt = f"""You are an expert AI Career Coach.
            The user wants to become a {target_role}.
            They are missing these core skills: {skill_names}.
            Generate a 30-day (4-week) learning roadmap focusing ONLY on these missing skills.
            Return ONLY a valid JSON object matching this schema exactly:
            {{
                "target_role": "{target_role}",
                "duration_weeks": 4,
                "weeks": [
                    {{
                        "week": 1,
                        "focus_areas": ["Skill 1", "Skill 2"],
                        "tasks": ["Task 1", "Task 2"]
                    }}
                ]
            }}
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
        
    current_week = 1
    skills_this_week = []
    
    for idx, skill in enumerate(missing_skills):
        skills_this_week.append(skill["missing_skill"])
        
        if len(skills_this_week) == 2 or idx == len(missing_skills) - 1:
            roadmap["weeks"].append({
                "week": current_week,
                "focus_areas": skills_this_week.copy(),
                "tasks": [
                    f"Read documentation on {skills_this_week[0]}",
                    f"Complete a tutorial integrating {', '.join(skills_this_week)}",
                    f"Build a mini-project"
                ]
            })
            current_week += 1
            skills_this_week = []
            
    return roadmap
