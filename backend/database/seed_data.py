import asyncio
from backend.database.postgres import AsyncSessionLocal, engine, Base
from backend.database import models

async def seed_roles():
    async with engine.begin() as conn:
        # Create all tables (assuming they don't exist yet or we just want to ensure they exist)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # Check if roles already exist
        from sqlalchemy.future import select
        result = await db.execute(select(models.Role))
        existing_roles = result.scalars().all()
        if existing_roles:
            print("Roles already seeded!")
            return

        roles_data = [
            {
                "name": "Data Scientist",
                "category": "Data",
                "min_experience_years": 3,
                "skills": [
                    {"name": "Python", "weight": 0.9, "is_core": True},
                    {"name": "SQL", "weight": 0.8, "is_core": True},
                    {"name": "Machine Learning", "weight": 0.9, "is_core": True},
                    {"name": "Pandas", "weight": 0.7, "is_core": False},
                    {"name": "Scikit-learn", "weight": 0.7, "is_core": False},
                    {"name": "Statistics", "weight": 0.8, "is_core": True}
                ]
            },
            {
                "name": "Machine Learning Engineer",
                "category": "AI",
                "min_experience_years": 3,
                "skills": [
                    {"name": "Python", "weight": 0.9, "is_core": True},
                    {"name": "Machine Learning", "weight": 0.9, "is_core": True},
                    {"name": "PyTorch", "weight": 0.8, "is_core": True},
                    {"name": "TensorFlow", "weight": 0.7, "is_core": False},
                    {"name": "Docker", "weight": 0.6, "is_core": False},
                    {"name": "SQL", "weight": 0.5, "is_core": False}
                ]
            },
            {
                "name": "GenAI Engineer",
                "category": "AI",
                "min_experience_years": 2,
                "skills": [
                    {"name": "Python", "weight": 0.9, "is_core": True},
                    {"name": "LangGraph", "weight": 0.8, "is_core": True},
                    {"name": "Vector Databases", "weight": 0.8, "is_core": True},
                    {"name": "LLM Evaluation", "weight": 0.8, "is_core": True},
                    {"name": "Agentic AI", "weight": 0.7, "is_core": True},
                    {"name": "Prompt Engineering", "weight": 0.6, "is_core": False}
                ]
            },
            {
                "name": "Data Analyst",
                "category": "Data",
                "min_experience_years": 1,
                "skills": [
                    {"name": "SQL", "weight": 0.9, "is_core": True},
                    {"name": "Excel", "weight": 0.7, "is_core": False},
                    {"name": "Python", "weight": 0.7, "is_core": True},
                    {"name": "Tableau", "weight": 0.8, "is_core": True},
                    {"name": "Data Visualization", "weight": 0.8, "is_core": True}
                ]
            },
            {
                "name": "AI Engineer",
                "category": "AI",
                "min_experience_years": 2,
                "skills": [
                    {"name": "Python", "weight": 0.9, "is_core": True},
                    {"name": "Machine Learning", "weight": 0.8, "is_core": True},
                    {"name": "Deep Learning", "weight": 0.8, "is_core": True},
                    {"name": "OpenAI API", "weight": 0.7, "is_core": False},
                    {"name": "FastAPI", "weight": 0.6, "is_core": False}
                ]
            },
            {
                "name": "MLOps Engineer",
                "category": "Engineering",
                "min_experience_years": 3,
                "skills": [
                    {"name": "Python", "weight": 0.8, "is_core": True},
                    {"name": "Docker", "weight": 0.9, "is_core": True},
                    {"name": "Kubernetes", "weight": 0.8, "is_core": True},
                    {"name": "CI/CD", "weight": 0.8, "is_core": True},
                    {"name": "AWS", "weight": 0.7, "is_core": False},
                    {"name": "MLflow", "weight": 0.7, "is_core": True}
                ]
            }
        ]

        for role_data in roles_data:
            role = models.Role(
                name=role_data["name"],
                category=role_data["category"],
                min_experience_years=role_data["min_experience_years"]
            )
            db.add(role)
            await db.flush() # get role.id
            
            for skill in role_data["skills"]:
                role_skill = models.RoleSkill(
                    role_id=role.id,
                    skill_name=skill["name"],
                    weight=skill["weight"],
                    is_core=skill["is_core"]
                )
                db.add(role_skill)
                
        # Also let's seed a fake user for testing if no users exist
        result = await db.execute(select(models.User))
        existing_users = result.scalars().all()
        if not existing_users:
            user = models.User(name="Bharath Singh", email="bharath@example.com", github_username="bharathsingh")
            db.add(user)
            await db.flush()
            
            user_skills = ["Python", "Machine Learning", "SQL", "TypeScript", "FastAPI", "React", "PostgreSQL", "MongoDB"]
            for s in user_skills:
                db.add(models.Skill(user_id=user.id, name=s, category="General"))
                
        await db.commit()
        print("Seed data loaded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_roles())
