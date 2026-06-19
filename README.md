# Formal Language Typing Game

[![CI](https://github.com/guduruharshita/formal-language-typing-game/actions/workflows/ci.yml/badge.svg)](https://github.com/guduruharshita/formal-language-typing-game/actions)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](pyproject.toml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](src/formal_game/api/main.py)
[![Challenges](https://img.shields.io/badge/Challenges-20-blueviolet)](src/formal_game/challenges.py)
[![Validators](https://img.shields.io/badge/Validators-21-orange)](src/formal_game/validator.py)
[![Tests](https://img.shields.io/badge/Tests-32%20passing-success?logo=pytest)](tests/)

Interactive typing game for **formal language theory** — players type strings that satisfy language rules under a countdown timer. 20 challenge types across regular languages, context-free languages, and string properties, with 3 difficulty levels and a persistent leaderboard.

---

## Why This Game

Most CS students study formal language theory for an exam and forget it immediately — DFAs, PDAs, and the Pumping Lemma remain abstract until you actively construct strings that *satisfy* those rules under pressure. This game forces you to internalize the difference between a regular language (which cannot count) and a context-free language (which can count one thing) by asking you to produce valid strings in under a minute. Typing `aaabbb` for `aⁿbⁿ` or `(()())` for balanced parentheses builds the same intuition that months of lecture notes can't.

---

## Game Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   Formal Language Typing Game                    │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                 Browser  (Dark-mode UI)                   │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │  60s Timer │ Challenge: aⁿbⁿ │ Score: 45 │ Streak: 3│ │  │
│  │  │  ──────────────────────────────────────────────────  │ │  │
│  │  │  Hint: Count must match — 'ab', 'aabb', 'aaabbb'    │ │  │
│  │  │  [ aaabbb                          ] [Submit]        │ │  │
│  │  └──────────────────────────────────────────────────────┘ │  │
│  └───────────────────────┬───────────────────────────────────┘  │
│                          │ POST /api/game/submit                 │
│  ┌───────────────────────▼───────────────────────────────────┐  │
│  │                  FastAPI (game.py router)                  │  │
│  │  SessionStore { session_id → GameSession }                 │  │
│  └───────────────────────┬───────────────────────────────────┘  │
│                          │                                       │
│         ┌────────────────┼─────────────────────┐                │
│         ▼                ▼                      ▼                │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────────────────┐  │
│  │validator.py │  │game_engine  │  │leaderboard.py (SQLite) │  │
│  │21 language  │  │GameSession  │  │GET /api/leaderboard    │  │
│  │validators   │  │60s timer    │  │POST /api/leaderboard   │  │
│  │dispatch dict│  │score / index│  │top-10 ranked scores    │  │
│  └─────────────┘  └─────────────┘  └────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Scoring Mechanics

```
Game Start (60 seconds on the clock)
      │
      ▼
Present Challenge ──────────────────────────────────────┐
      │                                                  │
      ▼                                                  │
Player submits answer                                    │
      │                                                  │
      ├── Correct ──▶  score += difficulty_points        │
      │                (Easy: +10, Medium: +15, Hard: +20)│
      │                                                  │
      └── Wrong ───▶  score -= 5  (floor: 0)             │
                      show: "Example: aaabbb"             │
                                                         │
      ◀──────────────── next challenge ──────────────────┘
      │
      ▼ (timer hits 0 OR 20 challenges exhausted)
Game Over → POST /api/leaderboard → SQLite rank
```

---

## Game Features

| Feature | Description |
|---------|-------------|
| **20 Challenge Types** | Regular (`a*b*`, `(01)*`, `aⁿbⁿ`, …), Context-Free (balanced parens, palindromes, `wwᴿ`, …), String Properties |
| **3 Difficulty Levels** | Easy (+10 pts), Medium (+15 pts), Hard (+20 pts) |
| **Scoring** | Correct: +difficulty points · Wrong: −5 points · floor at 0 |
| **60-Second Timer** | UUID-tracked sessions with server-side elapsed time |
| **Leaderboard** | SQLite-persisted top 10 scores by difficulty |
| **REST API** | Full game session management via JSON API |
| **Web UI** | Dark-mode HTML/JS frontend served from FastAPI |

---

## Challenge Coverage

| Category | Difficulty | Challenges |
|----------|-----------|-----------|
| **Regular Language** | Easy | `a*b*`, `(01)*`, `[ab]+`, `[01]*01` |
| **Regular Language** | Medium | `a+b+c+`, `∃ substring 101`, even-length binary, starts=ends, `1^(3k)` |
| **Regular Language** | Hard | even number of 1-bits, `a*b*c*` |
| **Context-Free** | Easy | Balanced `()`, Palindrome |
| **Context-Free** | Medium | `aⁿbⁿ`, equal `#a` and `#b` |
| **Context-Free** | Hard | `w·wᴿ`, `aⁿbᵐcⁿ` |
| **String Property** | Medium | No consecutive identical chars, contains 3-in-a-row |
| **String Property** | Hard | `(ab)+` or `(ba)+` |

---

## Quick Start

```bash
pip install -e .
uvicorn formal_game.api.main:app --reload
# Open http://localhost:8000
```

---

## API

```bash
# Start a game session
curl -X POST http://localhost:8000/api/game/start \
  -H "Content-Type: application/json" \
  -d '{"difficulty": "medium"}'
# {"session_id":"...","challenge":{"label":"aⁿbⁿ","description":"...","example":"aaabbb",...}}

# Submit an answer
curl -X POST http://localhost:8000/api/game/submit \
  -H "Content-Type: application/json" \
  -d '{"session_id": "...", "answer": "aaabbb"}'
# {"correct":true,"score_delta":15,"new_score":15,"next_challenge":{...},"remaining_seconds":52.1}

# List all challenges (filterable by difficulty or category)
curl "http://localhost:8000/api/game/challenges?difficulty=hard"

# Leaderboard
curl http://localhost:8000/api/leaderboard

# Submit score to leaderboard
curl -X POST http://localhost:8000/api/leaderboard \
  -H "Content-Type: application/json" \
  -d '{"name": "alice", "score": 145, "correct": 9, "difficulty": "hard"}'
```

---

## Project Structure

```
formal-language-typing-game/
│
├── src/formal_game/
│   ├── validator.py              # 21 formal language validation functions
│   ├── challenges.py             # 20 Challenge dataclasses (rule, label, hint, example, points)
│   ├── game_engine.py            # GameSession: 60s timer, UUID, scoring, challenge sequencing
│   └── api/
│       ├── main.py               # FastAPI app factory + lifespan (init_db on startup)
│       ├── state.py              # In-process session store {session_id: GameSession}
│       ├── static/index.html     # Dark-mode game UI (HTML + vanilla JS)
│       └── routers/
│           ├── game.py           # POST /start, /submit; GET /status/{id}, /challenges
│           └── leaderboard.py    # GET/POST /api/leaderboard (SQLite, ranked top-10)
│
├── game/                         # Legacy Tkinter desktop version (preserved)
│   ├── sentences.py
│   ├── validator.py
│   └── ui.py
│
├── tests/
│   ├── test_validator.py         # 20 unit tests — one per challenge rule
│   └── test_api.py               # 12 integration tests (start, submit, leaderboard)
│
├── .github/workflows/ci.yml      # Ruff lint + pytest on every push
├── pyproject.toml
└── main.py                       # Tkinter launcher
```

---

## Testing

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

```
tests/test_validator.py::TestRegularLanguages::test_a_star_b_star PASSED
tests/test_validator.py::TestRegularLanguages::test_alternating_01 PASSED
tests/test_validator.py::TestRegularLanguages::test_ends_in_01 PASSED
tests/test_validator.py::TestRegularLanguages::test_contains_101 PASSED
tests/test_validator.py::TestRegularLanguages::test_even_length_binary PASSED
tests/test_validator.py::TestRegularLanguages::test_divisible_by_3_unary PASSED
tests/test_validator.py::TestRegularLanguages::test_binary_even_ones PASSED
tests/test_validator.py::TestContextFreeLanguages::test_balanced_parens PASSED
tests/test_validator.py::TestContextFreeLanguages::test_palindrome PASSED
tests/test_validator.py::TestContextFreeLanguages::test_n_a_n_b PASSED
tests/test_validator.py::TestContextFreeLanguages::test_equal_ab PASSED
tests/test_validator.py::TestContextFreeLanguages::test_ww_reverse PASSED
tests/test_validator.py::TestContextFreeLanguages::test_n_a_m_b_n_c PASSED
tests/test_validator.py::TestStringProperties::test_no_consecutive PASSED
tests/test_validator.py::TestStringProperties::test_three_consecutive PASSED
tests/test_validator.py::TestStringProperties::test_alternating_ab PASSED
tests/test_api.py::test_start_game PASSED
tests/test_api.py::test_submit_correct PASSED
tests/test_api.py::test_submit_wrong_deducts_points PASSED
tests/test_api.py::test_leaderboard_empty PASSED
tests/test_api.py::test_submit_score_to_leaderboard PASSED

32 passed in 0.9s
```

---

## Formal Language Theory Background

| Language Class | Accepted By | Key Property | In-Game Example |
|---------------|-------------|-------------|-----------------|
| **Regular** | DFA / NFA / Regex | Cannot count | `a*b*`, `(01)*`, `1^(3k)` |
| **Context-Free** | Pushdown Automaton | Can count one thing | `aⁿbⁿ`, balanced `()`, palindrome |
| **Context-Sensitive** | Linear Bounded Automaton | Can count two things | `aⁿbⁿcⁿ` (hardest challenge) |

Regular languages cannot enforce equal counts — `aⁿbⁿ` is the canonical CFL and the classic Pumping Lemma example. Typing `aaabbb` correctly (and getting it wrong once because you mismatched the count) teaches that boundary faster than any lecture.

---

## Validation Architecture

All 21 validators live in `validator.py` behind a single dispatch dictionary — no conditionals in the router, no class hierarchy, just a `str → Callable` map:

```python
_RULES: dict[str, Callable[[str], bool]] = {
    "a_star_b_star":    _a_star_b_star,
    "n_a_n_b":          _n_a_n_b,
    "balanced_parens":  _balanced_parens,
    "ww_reverse":       _ww_reverse,
    # ...
}

def validate(rule: str, s: str) -> bool:
    fn = _RULES.get(rule)
    return fn(s) if fn is not None else False
```

Adding a new language rule requires one function and one dict entry — no changes to the API, engine, or UI.

---

## Skills Demonstrated

| Skill | Evidence |
|-------|---------|
| **Formal Language Theory** | 21 validators covering RL, CFL, and string properties; theory background in README |
| **FastAPI** | App factory, lifespan events, Pydantic v2 schemas, StaticFiles |
| **Game State Management** | Timed sessions with UUID tracking, challenge sequencing, score floor |
| **SQLite** | Raw SQL with context-manager, leaderboard with ranked `COUNT(*)` queries |
| **Frontend** | Vanilla JS + CSS variables dark-mode game UI, no framework dependencies |
| **Python Packaging** | `pyproject.toml`, `src/` layout, `StrEnum`, frozen dataclasses |
| **Testing** | 32 pytest tests — unit tests per language class + API integration tests |
| **CI/CD** | GitHub Actions: ruff lint + pytest |

---

**Harshita Guduru** — [GitHub](https://github.com/guduruharshita) · [LinkedIn](https://linkedin.com/in/guduruharshita) · [Email](mailto:guduruharshita2001@gmail.com)
