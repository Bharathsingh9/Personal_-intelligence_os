from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database.postgres import engine, Base
import backend.database.models  # Register models

from backend.api import ingestion, profile, analytics, intelligence, market, copilot, simulator, reports

app = FastAPI(title="Personal Intelligence OS", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingestion.router)
app.include_router(profile.router)
app.include_router(analytics.router)
app.include_router(intelligence.router)
app.include_router(market.router)
app.include_router(copilot.router)
app.include_router(simulator.router)
app.include_router(reports.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def read_root():
    return {"message": "Welcome to Personal Intelligence OS API"}
