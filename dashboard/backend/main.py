from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from core.agents.runner import SFDRunner

app = FastAPI(title="SFD — Space for Debate API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_runner: SFDRunner | None = None


def _get_runner() -> SFDRunner:
    global _runner
    if _runner is None:
        _runner = SFDRunner()
    return _runner


class MIRequest(BaseModel):
    mi: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/debate")
def debate(request: MIRequest):
    if not request.mi.strip():
        raise HTTPException(status_code=400, detail="MI non può essere vuoto")
    result = _get_runner().run(request.mi.strip())
    return result
