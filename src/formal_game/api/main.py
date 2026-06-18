from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from formal_game.api.routers import game, leaderboard
from formal_game.api.routers.leaderboard import init_db

STATIC_DIR = Path(__file__).parent / "static"


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        init_db()
        yield

    app = FastAPI(
        title="Formal Language Typing Game",
        version="2.0.0",
        description=(
            "Interactive typing game for formal language theory: regular languages, "
            "context-free grammars, and string properties. 20 challenge types, "
            "3 difficulty levels, persistent leaderboard."
        ),
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["health"])
    def health() -> dict:
        return {"status": "ok"}

    app.include_router(game.router)
    app.include_router(leaderboard.router)

    if STATIC_DIR.exists():
        app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

    return app


app = create_app()
