from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from backend.intelligence.simulator import run_simulation

router = APIRouter(prefix="/api/v1/simulator", tags=["Career Simulator"])

class SimulationRequest(BaseModel):
    current_score: float
    hypothetical_skills: List[str]
    target_role: str

@router.post("/run")
async def simulate_career(req: SimulationRequest):
    return run_simulation(req.current_score, req.hypothetical_skills, req.target_role)
