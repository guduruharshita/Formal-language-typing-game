# Formal Language Typing Game

[![CI](https://github.com/guduruharshita/formal-language-typing-game/actions/workflows/ci.yml/badge.svg)](https://github.com/guduruharshita/formal-language-typing-game/actions)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](pyproject.toml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](src/formal_game/api/main.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Interactive typing game for **formal language theory** — players type strings that satisfy language rules under a countdown timer. 20 challenge types across regular languages, context-free languages, and string properties, with 3 difficulty levels and a persistent leaderboard.

## Game Features

| Feature | Description |
|---------|-------------|
| **20 Challenge Types** | Regular (a\*b\*, (01)\*, aⁿbⁿ, …), Context-Free (balanced parens, palindromes, wwᴿ, …), String Properties |
| **3 Difficulty Levels** | Easy (+10 pts), Medium (+15 pts), Hard (+20 pts) |
| **Scoring** | Correct: +difficulty points · Wrong: −5 points · 60 second timer |
| **Leaderboard** | SQLite-persisted top 10 scores by difficulty |
| **REST API** | Full game session management via JSON API |
| **Web UI** | Dark-mode HTML/JS frontend served from FastAPI |

## Challenge Coverage

| Category | Examples |
|----------|---------|
| **Regular** | `a*b*`, `(01)*`, `[01]*01`, `a+b+c+`, `1^(3k)`, even 1-bits |
| **Context-Free** | Balanced `()`, Palindrome, `aⁿbⁿ`, `equal #a #b`, `wwᴿ`, `aⁿbᵐcⁿ` |
| **String Properties** | No consecutive chars, 3-in-a-row, `(ab)+`, starts=ends |

## Quick Start

```bash
pip install -e .
uvicorn formal_game.api.main:app --reload
# Open http://localhost:8000
```

## API

```bash
# Start a game
curl -X POST http://localhost:8000/api/game/start \
  -H "Content-Type: application/json" \
  -d '{"difficulty": "medium"}'
# {"session_id":"...","challenge":{"label":"aⁿbⁿ","description":"...","example":"aaabbb",...}}

# Submit an answer
curl -X POST http://localhost:8000/api/game/submit \
  -H "Content-Type: application/json" \
  -d '{"session_id": "...", "answer": "aaabbb"}'
# {"correct":true,"score_delta":15,"new_score":15,"next_challenge":{...},"remaining_seconds":52.1}

# Get challenge list (filterable by difficulty/category)
curl "http://localhost:8000/api/game/challenges?difficulty=hard"

# Leaderboard
curl http://localhost:8000/api/leaderboard
```

## Project Structure

```
formal-language-typing-game/
│
├── src/formal_game/
│   ├── validator.py              # 21 formal language validation functions
│   ├── challenges.py             # 20 Challenge dataclasses with description/hint/example
│   ├── game_engine.py            # GameSession: scoring, timer, challenge sequencing
│   └── api/
│       ├── main.py               # FastAPI app factory + lifespan
│       ├── state.py              # In-process session store
│       ├── static/index.html     # Dark-mode game UI (HTML + vanilla JS)
│       └── routers/
│           ├── game.py           # POST /start, /submit; GET /status, /challenges
│           └── leaderboard.py    # GET/POST /api/leaderboard (SQLite persistence)
│
├── game/                         # Legacy Tkinter desktop version
│   ├── sentences.py
│   ├── validator.py
│   └── ui.py
│
├── tests/
│   ├── test_validator.py         # 20 validator unit tests
│   └── test_api.py               # 12 API integration tests
│
├── .github/workflows/ci.yml
├── pyproject.toml
└── main.py                       # Tkinter launcher
```

## Testing

```bash
pip install -e ".[dev]"
pytest tests/ -v
# 32 passed
```

## Formal Language Theory Background

| Language Class | Accepted By | Key Property | Example |
|---------------|-------------|-------------|---------|
| **Regular** | DFA / NFA / Regex | Cannot count | `a*b*`, `(01)*` |
| **Context-Free** | Pushdown Automaton | Can count one thing | `aⁿbⁿ`, balanced `()` |
| **Context-Sensitive** | Linear Bounded Automaton | Can count two things | `aⁿbⁿcⁿ` |

Regular languages cannot enforce equal counts (e.g., #a = #b), making `aⁿbⁿ` a canonical CFL and a classic Pumping Lemma example — challenging players to understand the boundary between language classes.

## Skills Demonstrated

| Skill | Evidence |
|-------|---------|
| **Formal Language Theory** | 21 validators covering RL, CFL, and string properties with edge cases |
| **FastAPI** | App factory, lifespan events, Pydantic v2 schemas, dependency injection |
| **Game State Management** | Timed sessions with UUID tracking, challenge sequencing, score persistence |
| **SQLite** | Raw SQL with context-manager connection, leaderboard with ranked queries |
| **Frontend** | Vanilla JS + CSS variables dark-mode game UI served via StaticFiles |
| **Python Packaging** | `pyproject.toml`, `src/` layout, StrEnum, dataclasses |
| **Testing** | 32 pytest tests — unit tests per language class + API integration tests |
| **CI/CD** | GitHub Actions: ruff lint + pytest |

---

**Harshita Guduru** — [GitHub](https://github.com/guduruharshita) · [LinkedIn](https://linkedin.com/in/guduruharshita) · [Email](mailto:guduruharshita2001@gmail.com)
