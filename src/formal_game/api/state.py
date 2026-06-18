"""Shared in-process session store (swap for Redis in production)."""

from formal_game.game_engine import GameSession

_sessions: dict[str, GameSession] = {}


def get_sessions() -> dict[str, GameSession]:
    return _sessions
