"""Game session endpoints."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from formal_game.api.state import get_sessions
from formal_game.challenges import CHALLENGES, Category, Difficulty
from formal_game.game_engine import GameSession

router = APIRouter(prefix="/api/game", tags=["game"])

SessionStore = Annotated[dict[str, GameSession], Depends(get_sessions)]


# ── Schemas ──────────────────────────────────────────────────────────────────

class StartRequest(BaseModel):
    difficulty: Difficulty = Difficulty.EASY


class ChallengeOut(BaseModel):
    rule: str
    label: str
    description: str
    hint: str
    example: str
    category: str
    difficulty: str
    points: int


class StartResponse(BaseModel):
    session_id: str
    difficulty: str
    challenge: ChallengeOut | None
    remaining_seconds: float
    score: int


class SubmitRequest(BaseModel):
    session_id: str
    answer: str


class SubmitResponse(BaseModel):
    correct: bool
    score_delta: int
    new_score: int
    explanation: str
    next_challenge: ChallengeOut | None
    remaining_seconds: float
    finished: bool


class StatusResponse(BaseModel):
    session_id: str
    score: int
    correct: int
    incorrect: int
    remaining_seconds: float
    finished: bool
    challenge: ChallengeOut | None


class ChallengeListItem(BaseModel):
    rule: str
    label: str
    description: str
    category: str
    difficulty: str
    points: int


# ── Helpers ──────────────────────────────────────────────────────────────────

def _challenge_out(c) -> ChallengeOut:
    return ChallengeOut(
        rule=c.rule,
        label=c.label,
        description=c.description,
        hint=c.hint,
        example=c.example,
        category=c.category,
        difficulty=c.difficulty,
        points=c.points,
    )


# ── Routes ───────────────────────────────────────────────────────────────────

@router.post("/start", response_model=StartResponse)
def start_game(payload: StartRequest, sessions: SessionStore) -> StartResponse:
    session_id = str(uuid.uuid4())
    session = GameSession(session_id=session_id, difficulty=payload.difficulty)
    sessions[session_id] = session
    ch = session.current_challenge
    return StartResponse(
        session_id=session_id,
        difficulty=payload.difficulty,
        challenge=_challenge_out(ch) if ch else None,
        remaining_seconds=session.remaining_seconds,
        score=0,
    )


@router.post("/submit", response_model=SubmitResponse)
def submit_answer(payload: SubmitRequest, sessions: SessionStore) -> SubmitResponse:
    session = sessions.get(payload.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    result = session.submit(payload.answer)
    next_ch = session.current_challenge

    return SubmitResponse(
        correct=result.correct,
        score_delta=result.score_delta,
        new_score=result.new_score,
        explanation=result.explanation,
        next_challenge=_challenge_out(next_ch) if next_ch else None,
        remaining_seconds=session.remaining_seconds,
        finished=session.finished or session.is_time_up,
    )


@router.get("/status/{session_id}", response_model=StatusResponse)
def game_status(session_id: str, sessions: SessionStore) -> StatusResponse:
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    ch = session.current_challenge
    return StatusResponse(
        session_id=session_id,
        score=session.score,
        correct=session.correct,
        incorrect=session.incorrect,
        remaining_seconds=session.remaining_seconds,
        finished=session.finished or session.is_time_up,
        challenge=_challenge_out(ch) if ch else None,
    )


@router.get("/challenges", response_model=list[ChallengeListItem])
def list_challenges(
    category: Category | None = None,
    difficulty: Difficulty | None = None,
) -> list[ChallengeListItem]:
    results = CHALLENGES[:]
    if category:
        results = [c for c in results if c.category == category]
    if difficulty:
        results = [c for c in results if c.difficulty == difficulty]
    return [
        ChallengeListItem(
            rule=c.rule,
            label=c.label,
            description=c.description,
            category=c.category,
            difficulty=c.difficulty,
            points=c.points,
        )
        for c in results
    ]
