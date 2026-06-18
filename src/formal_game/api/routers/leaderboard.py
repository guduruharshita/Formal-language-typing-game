"""Leaderboard endpoints — persist top scores in SQLite."""

import sqlite3
import time
from collections.abc import Generator
from contextlib import contextmanager

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])

_DB_PATH = "leaderboard.db"


@contextmanager
def _db() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with _db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                name      TEXT    NOT NULL,
                score     INTEGER NOT NULL,
                correct   INTEGER NOT NULL DEFAULT 0,
                difficulty TEXT   NOT NULL DEFAULT 'easy',
                played_at INTEGER NOT NULL
            )
        """)


# ── Schemas ──────────────────────────────────────────────────────────────────

class ScoreSubmit(BaseModel):
    name: str
    score: int
    correct: int = 0
    difficulty: str = "easy"


class ScoreEntry(BaseModel):
    rank: int
    name: str
    score: int
    correct: int
    difficulty: str
    played_at: int


# ── Routes ───────────────────────────────────────────────────────────────────

@router.get("", response_model=list[ScoreEntry])
def get_leaderboard(limit: int = 10) -> list[ScoreEntry]:
    with _db() as conn:
        rows = conn.execute(
            "SELECT * FROM scores ORDER BY score DESC, correct DESC LIMIT ?",
            (min(limit, 50),),
        ).fetchall()
    return [
        ScoreEntry(
            rank=i + 1,
            name=row["name"],
            score=row["score"],
            correct=row["correct"],
            difficulty=row["difficulty"],
            played_at=row["played_at"],
        )
        for i, row in enumerate(rows)
    ]


@router.post("", response_model=ScoreEntry, status_code=201)
def submit_score(payload: ScoreSubmit) -> ScoreEntry:
    name = payload.name.strip()[:30] or "Anonymous"
    with _db() as conn:
        ts = int(time.time())
        vals = (name, max(0, payload.score), max(0, payload.correct), payload.difficulty, ts)
        conn.execute(
            "INSERT INTO scores (name, score, correct, difficulty, played_at) VALUES (?,?,?,?,?)",
            vals,
        )
        rank_row = conn.execute(
            "SELECT COUNT(*) FROM scores WHERE score > ?", (payload.score,)
        ).fetchone()
    rank = rank_row[0] + 1
    return ScoreEntry(
        rank=rank,
        name=name,
        score=payload.score,
        correct=payload.correct,
        difficulty=payload.difficulty,
        played_at=int(time.time()),
    )
