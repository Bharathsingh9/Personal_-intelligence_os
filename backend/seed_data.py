import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.postgres import AsyncSessionLocal, engine, Base
from backend.database.models import Role, RoleSkill

async def seed_roles():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        roles_data = [
            {
                "name": "Data Scientist",
                "category": "Data",
                "skills": [
                    {"name": "Python", "weight": 2.0, "is_core": True},
                    {"name": "Machine Learning", "weight": 3.0, "is_core": True},
                    {"name": "SQL", "weight": 2.0, "is_core": True},
                    {"name": "Pandas", "weight": 1.5, "is_core": False},
                    {"name": "Deep Learning", "weight": 2.0, "is_core": False}
                ]
            },
            {
                "name": "ML Engineer",
                "category": "Engineering",
                "skills": [
                    {"name": "Python", "weight": 2.0, "is_core": True},
                    {"name": "Machine Learning", "weight": 2.0, "is_core": True},
                    {"name": "Docker", "weight": 2.0, "is_core": True},
                    {"name": "MLOps", "weight": 3.0, "is_core": True},
                    {"name": "PyTorch", "weight": 2.0, "is_core": False}
                ]
            },
            {
                "name": "GenAI Engineer",
                "category": "Engineering",
                "skills": [
                    {"name": "Python", "weight": 2.0, "is_core": True},
                    {"name": "LLM Evaluation", "weight": 3.0, "is_core": True},
                    {"name": "LangGraph", "weight": 3.0, "is_core": True},
                    {"name": "Vector Databases", "weight": 3.0, "is_core": True},
                    {"name": "Agentic AI", "weight": 3.0, "is_core": True},
                    {"name": "FastAPI", "weight": 1.5, "is_core": False}
                ]
            },
            {
                "name": "Data Analyst",
                "category": "Data",
                "skills": [
                    {"name": "SQL", "weight": 3.0, "is_core": True},
                    {"name": "Excel", "weight": 2.0, "is_core": True},
                    {"name": "Tableau", "weight": 2.0, "is_core": True},
                    {"name": "Python", "weight": 1.5, "is_core": False}
                ]
            },
            {
                "name": "AI Engineer",
                "category": "Engineering",
                "skills": [
                    {"name": "Python", "weight": 2.0, "is_core": True},
                    {"name": "Deep Learning", "weight": 3.0, "is_core": True},
                    {"name": "FastAPI", "weight": 2.0, "is_core": True},
                    {"name": "Docker", "weight": 2.0, "is_core": False}
                ]
            },
            {
                "name": "MLOps Engineer",
                "category": "Engineering",
                "skills": [
                    {"name": "Docker", "weight": 3.0, "is_core": True},
                    {"name": "Kubernetes", "weight": 3.0, "is_core": True},
                    {"name": "CI/CD", "weight": 3.0, "is_core": True},
                    {"name": "Python", "weight": 2.0, "is_core": True},
                    {"name": "Terraform", "weight": 2.0, "is_core": False}
                ]
            }
        ]

        for role_data in roles_data:
            # Check if role exists
            from sqlalchemy.future import select
            result = await db.execute(select(Role).where(Role.name == role_data["name"]))
            existing_role = result.scalar_one_or_none()
            
            if not existing_role:
                print(f"Adding Role: {role_data['name']}")
                new_role = Role(name=role_data["name"], category=role_data["category"])
                db.add(new_role)
                await db.flush()  # To get the ID
                
                for skill in role_data["skills"]:
                    rs = RoleSkill(
                        role_id=new_role.id,
                        skill_name=skill["name"],
                        weight=skill["weight"],
                        is_core=skill["is_core"]
                    )
                    db.add(rs)
            else:
                print(f"Role already exists: {role_data['name']}")

        await db.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_roles())
