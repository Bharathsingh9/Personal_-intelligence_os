import httpx
from typing import Dict, Any

async def analyze_github_profile(username: str, token: str = None) -> Dict[str, Any]:
    """Fetch and analyze GitHub profile using the REST API."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    async with httpx.AsyncClient(headers=headers) as client:
        # Fetch user profile
        user_url = f"https://api.github.com/users/{username}"
        user_resp = await client.get(user_url)
        
        if user_resp.status_code != 200:
            return {"error": "User not found or API limit reached"}
            
        user_data = user_resp.json()
        
        # Fetch repos
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
        repos_resp = await client.get(repos_url)
        
        repos_data = []
        if repos_resp.status_code == 200:
            repos_data = repos_resp.json()

        # Calculate language stats and collect projects
        language_stats = {}
        projects = []
        
        for repo in repos_data:
            if repo.get("fork"):
                continue
                
            lang = repo.get("language")
            if lang:
                language_stats[lang] = language_stats.get(lang, 0) + 1
                
            projects.append({
                "name": repo.get("name"),
                "description": repo.get("description"),
                "technologies": [lang] if lang else [],
                "source": "GitHub"
            })

        # Sort languages by frequency
        top_languages = dict(sorted(language_stats.items(), key=lambda item: item[1], reverse=True))

        return {
            "github_username": username,
            "github_stats": {
                "followers": user_data.get("followers", 0),
                "public_repos": user_data.get("public_repos", 0)
            },
            "top_languages": top_languages,
            "projects": projects
        }
