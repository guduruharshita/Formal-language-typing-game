import tkinter as tk
import random
from .sentences import SENTENCES
from .validator import validate


class TypingGame:
    DURATION = 45

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Formal Language Typing Game")
        self.root.configure(bg="#1e1e2e")
        self._score = 0
        self._time_left = self.DURATION
        self._used: list = []
        self._current: dict = {}
        self._timer_id = None
        self._build_ui()

    def _build_ui(self):
        tk.Label(self.root, text="Formal Language Typing Game",
                 font=("Helvetica", 18, "bold"), bg="#1e1e2e", fg="#cdd6f4").pack(pady=10)
        self.sentence_lbl = tk.Label(self.root, text="Press Start",
                                     font=("Courier", 22, "bold"), bg="#1e1e2e", fg="#89b4fa")
        self.sentence_lbl.pack(pady=15)
        self.rule_lbl = tk.Label(self.root, text="", font=("Helvetica", 13),
                                 bg="#1e1e2e", fg="#a6e3a1")
        self.rule_lbl.pack()
        self.entry = tk.Entry(self.root, font=("Courier", 18), width=24,
                              bg="#313244", fg="#cdd6f4", insertbackground="white")
        self.entry.pack(pady=12)
        self.entry.bind("<Return>", self._check)

        row = tk.Frame(self.root, bg="#1e1e2e"); row.pack(pady=4)
        self.timer_lbl = tk.Label(row, text=f"{self.DURATION}s", font=("Helvetica", 14),
                                  bg="#1e1e2e", fg="#fab387", width=6)
        self.timer_lbl.pack(side=tk.LEFT, padx=8)
        self.score_lbl = tk.Label(row, text="Score: 0", font=("Helvetica", 14),
                                  bg="#1e1e2e", fg="#f38ba8")
        self.score_lbl.pack(side=tk.LEFT, padx=8)

        self.feedback_lbl = tk.Label(self.root, text="", font=("Helvetica", 13),
                                     bg="#1e1e2e", fg="white")
        self.feedback_lbl.pack(pady=4)

        btn_row = tk.Frame(self.root, bg="#1e1e2e"); btn_row.pack(pady=12)
        self.start_btn = tk.Button(btn_row, text="Start", command=self._start,
                                   font=("Helvetica", 12), bg="#89b4fa", fg="#1e1e2e", padx=10)
        self.start_btn.pack(side=tk.LEFT, padx=6)
        self.skip_btn = tk.Button(btn_row, text="Skip", command=self._next,
                                  font=("Helvetica", 12), bg="#585b70", fg="#cdd6f4", padx=10)
        self.skip_btn.pack(side=tk.LEFT, padx=6)
        self.skip_btn.pack_forget()

    def _start(self):
        self._score = 0
        self._time_left = self.DURATION
        self._used = []
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
        self._refresh_score()
        self._refresh_timer()
        self.entry.config(state=tk.NORMAL)
        self.feedback_lbl.config(text="")
        self.skip_btn.pack(side=tk.LEFT, padx=6)
        self._next()
        self._tick()

    def _tick(self):
        if self._time_left <= 0:
            self._end()
            return
        self._time_left -= 1
        self._refresh_timer()
        self._timer_id = self.root.after(1000, self._tick)

    def _next(self):
        pool = [s for s in SENTENCES if s not in self._used]
        if not pool:
            self._used, pool = [], SENTENCES[:]
        self._current = random.choice(pool)
        self._used.append(self._current)
        self.sentence_lbl.config(text=self._current["sentence"])
        self.rule_lbl.config(text=f"Rule: {self._current['label']}")
        self.entry.delete(0, tk.END)
        self.feedback_lbl.config(text="")

    def _check(self, _=None):
        user = self.entry.get().strip()
        if validate(user, self._current["rule"]):
            self._score += 10
            self.feedback_lbl.config(text="Correct! ✔", fg="#a6e3a1")
        else:
            self._score = max(0, self._score - 5)
            self.feedback_lbl.config(text="Wrong! ✘", fg="#f38ba8")
        self._refresh_score()
        self.root.after(800, self._next)

    def _end(self):
        self.sentence_lbl.config(text="⏱ Time's up!")
        self.rule_lbl.config(text=f"Final Score: {self._score}")
        self.entry.config(state=tk.DISABLED)
        self.skip_btn.pack_forget()
        self.start_btn.config(text="Play Again", command=self._start)

    def _refresh_score(self):
        self.score_lbl.config(text=f"Score: {self._score}")

    def _refresh_timer(self):
        self.timer_lbl.config(text=f"{self._time_left}s")
