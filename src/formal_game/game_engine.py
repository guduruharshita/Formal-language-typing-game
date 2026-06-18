"""Game session management — challenge sequencing, scoring, and time tracking."""

import random
import time
from dataclasses import dataclass, field

from formal_game.challenges import CHALLENGES, Challenge, Difficulty
from formal_game.validator import validate

GAME_DURATION_SECONDS = 60
WRONG_ANSWER_PENALTY = 5
MAX_CHALLENGES_PER_GAME = 20


@dataclass
class SubmitResult:
    correct: bool
    score_delta: int
    new_score: int
    explanation: str


@dataclass
class GameSession:
    session_id: str
    difficulty: Difficulty
    started_at: float = field(default_factory=time.time)
    score: int = 0
    correct: int = 0
    incorrect: int = 0
    challenge_index: int = 0
    _challenges: list[Challenge] = field(default_factory=list)
    finished: bool = False

    def __post_init__(self) -> None:
        pool = [c for c in CHALLENGES if c.difficulty == self.difficulty]
        if not pool:
            pool = CHALLENGES[:]
        random.shuffle(pool)
        repeat = (MAX_CHALLENGES_PER_GAME // len(pool)) + 2
        self._challenges = (pool * repeat)[:MAX_CHALLENGES_PER_GAME]

    @property
    def current_challenge(self) -> Challenge | None:
        if self.challenge_index >= len(self._challenges):
            return None
        return self._challenges[self.challenge_index]

    @property
    def elapsed_seconds(self) -> float:
        return time.time() - self.started_at

    @property
    def remaining_seconds(self) -> float:
        return max(0.0, GAME_DURATION_SECONDS - self.elapsed_seconds)

    @property
    def is_time_up(self) -> bool:
        return self.elapsed_seconds >= GAME_DURATION_SECONDS

    def submit(self, answer: str) -> SubmitResult:
        if self.finished or self.is_time_up:
            self.finished = True
            return SubmitResult(
                correct=False,
                score_delta=0,
                new_score=self.score,
                explanation="Game over — time's up!",
            )

        challenge = self.current_challenge
        if challenge is None:
            self.finished = True
            return SubmitResult(
                correct=False,
                score_delta=0,
                new_score=self.score,
                explanation="No more challenges.",
            )

        is_correct = validate(challenge.rule, answer.strip())
        if is_correct:
            delta = challenge.points
            self.correct += 1
            explanation = f"Correct! +{delta} points"
        else:
            delta = -WRONG_ANSWER_PENALTY
            self.incorrect += 1
            explanation = (
                f"Wrong. Penalty: {WRONG_ANSWER_PENALTY} points. Example: {challenge.example}"
            )

        self.score = max(0, self.score + delta)
        self.challenge_index += 1

        if self.challenge_index >= len(self._challenges):
            self.finished = True

        return SubmitResult(
            correct=is_correct,
            score_delta=delta,
            new_score=self.score,
            explanation=explanation,
        )
