import tkinter as tk
import random
from .sentences import SENTENCES
from .validator import validate

class TypingGame:
    GAME_DURATION = 45

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Formal Language Typing Game")
        self.root.configure(bg="#1e1e2e")
        self._score = 0
        self._time_left = self.GAME_DURATION
        self._used: list = []
        self._current: dict = {}
        self._timer_id = None
        self._build_ui()

    def _build_ui(self):
        tk.Label(self.root, text="Formal Language Typing Game",
                 font=("Helvetica", 20, "bold"), bg="#1e1e2e", fg="#cdd6f4").pack(pady=10)
        self.sentence_label = tk.Label(self.root, text="Press Start to begin",
                                       font=("Courier", 22, "bold"), bg="#1e1e2e", fg="#89b4fa")
        self.sentence_label.pack(pady=20)
        self.rule_label = tk.Label(self.root, text="", font=("Helvetica", 13),
                                   bg="#1e1e2e", fg="#a6e3a1")
        self.rule_label.pack()
        self.entry = tk.Entry(self.root, font=("Courier", 18), width=25,
                              bg="#313244", fg="#cdd6f4", insertbackground="white")
        self.entry.pack(pady=15)
        self.entry.bind("<Return>", self._check)
        row = tk.Frame(self.root, bg="#1e1e2e")
        row.pack(pady=5)
        self.timer_label = tk.Label(row, text=f"{self.GAME_DURATION}s", font=("Helvetica", 14),
                                    bg="#1e1e2e", fg="#fab387", width=8)
        self.timer_label.pack(side=tk.LEFT, padx=10)
        self.score_label = tk.Label(row, text="Score: 0", font=("Helvetica", 14),
                                    bg="#1e1e2e", fg="#f38ba8")
        self.score_label.pack(side=tk.LEFT, padx=10)
        self.feedback_label = tk.Label(self.root, text="", font=("Helvetica", 14),
                                       bg="#1e1e2e", fg="white")
        self.feedback_label.pack(pady=5)
        btn_row = tk.Frame(self.root, bg="#1e1e2e")
        btn_row.pack(pady=15)
        self.start_btn = tk.Button(btn_row, text="Start", command=self._start,
                                   font=("Helvetica", 13), bg="#89b4fa", fg="#1e1e2e", padx=12)
        self.start_btn.pack(side=tk.LEFT, padx=8)
        self.skip_btn = tk.Button(btn_row, text="Skip", command=self._next_sentence,
                                  font=("Helvetica", 13), bg="#585b70", fg="#cdd6f4", padx=12)
        self.skip_btn.pack(side=tk.LEFT, padx=8)
        self.skip_btn.pack_forget()

    def _start(self):
        self._score = 0
        self._time_left = self.GAME_DURATION
        self._used = []
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
        self._refresh_score()
        self._refresh_timer()
        self.entry.config(state=tk.NORMAL)
        self.feedback_label.config(text="")
        self.skip_btn.pack(side=tk.LEFT, padx=8)
        self._next_sentence()
        self._tick()

    def _tick(self):
        if self._time_left <= 0:
            self._end_game()
            return
        self._time_left -= 1
        self._refresh_timer()
        self._timer_id = self.root.after(1000, self._tick)

    def _refresh_timer(self):
        self.timer_label.config(text=f"{self._time_left}s")

    def _refresh_score(self):
        self.score_label.config(text=f"Score: {self._score}")

    def _next_sentence(self):
        available = [s for s in SENTENCES if s not in self._used]
        if not available:
            self._used = []
            available = SENTENCES[:]
        self._current = random.choice(available)
        self._used.append(self._current)
        self.sentence_label.config(text=self._current["sentence"])
        self.rule_label.config(text=f"Rule: {self._current['label']}")
        self.entry.delete(0, tk.END)
        self.feedback_label.config(text="")

    def _check(self, _event=None):
        user_input = self.entry.get().strip()
        if validate(user_input, self._current["rule"]):
            self._score += 10
            self.feedback_label.config(text="Correct!", fg="#a6e3a1")
        else:
            self._score = max(0, self._score - 5)
            self.feedback_label.config(text="Wrong!", fg="#f38ba8")
        self._refresh_score()
        self.root.after(800, self._next_sentence)

    def _end_game(self):
        self.sentence_label.config(text="Time's up!")
        self.rule_label.config(text=f"Final Score: {self._score}")
        self.entry.config(state=tk.DISABLED)
        self.skip_btn.pack_forget()
        self.start_btn.config(text="Play Again", command=self._start)
