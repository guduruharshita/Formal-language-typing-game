import tkinter as tk
import random
import re
import time

class TypingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Formal Language Typing Game")

        self.sentences = [
            {"sentence": "aaaabbbb", "rule": "a*b*"},
            {"sentence": "(())", "rule": "balanced_parentheses"},
            {"sentence": "racecar", "rule": "palindrome"},
            {"sentence": "01", "rule": "alternating_01"},
            {"sentence": "00101", "rule": "contains_101"},
            {"sentence": "01101", "rule": "ends_in_01"},
            {"sentence": "aaabbbccc", "rule": "a+b+c"},
            {"sentence": "aabbbccc", "rule": "a*b*c"},
            {"sentence": "aaabccc", "rule": "a*b+c"}
        ]

        self.used_sentences = []
        self.current_sentence = {}
        self.score = 0
        self.time_left = 45

        self.sentence_label = tk.Label(root, text="", font=("Helvetica", 18))
        self.sentence_label.pack(pady=20)

        self.entry = tk.Entry(root, font=("Helvetica", 16))
        self.entry.pack(pady=20)
        self.entry.bind("<Return>", self.check_sentence)

        self.timer_label = tk.Label(root, text="45 seconds remaining", font=("Helvetica", 14))
        self.timer_label.pack(pady=10)

        self.score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 14))
        self.score_label.pack(pady=10)

        self.feedback_label = tk.Label(root, text="", font=("Helvetica", 14), fg="red")
        self.feedback_label.pack(pady=10)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        self.start_button = tk.Button(self.button_frame, text="Start Game", command=self.start_game, font=("Helvetica", 14))
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.skip_button = tk.Button(self.button_frame, text="Skip", command=self.skip_sentence, font=("Helvetica", 14))
        self.skip_button.pack(side=tk.LEFT, padx=5)
        self.skip_button.pack_forget()  # Hide skip button initially

    def start_game(self):
        self.score = 0
        self.time_left = 45
        self.used_sentences = []
        self.update_score()
        self.update_timer()
        self.next_sentence()
        self.start_timer()
        self.feedback_label.config(text="")
        self.start_button.config(text="Enter", command=self.check_sentence)
        self.skip_button.pack()  # Show skip button after the game starts

    def start_timer(self):
        self.timer_running = True
        self.update_clock()

    def update_clock(self):
        if self.time_left <= 0:
            self.timer_running = False
            self.end_game()
        else:
            self.time_left -= 1
            self.update_timer()
            self.root.after(1000, self.update_clock)

    def update_timer(self):
        self.timer_label.config(text=f"{self.time_left} seconds remaining")

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def next_sentence(self):
        if len(self.used_sentences) == len(self.sentences):
            self.used_sentences = []

        available_sentences = [s for s in self.sentences if s not in self.used_sentences]
        self.current_sentence = random.choice(available_sentences)
        self.used_sentences.append(self.current_sentence)
        
        self.sentence_label.config(text=self.current_sentence["sentence"])
        self.entry.delete(0, tk.END)
        self.feedback_label.config(text="")

    def check_sentence(self, event=None):
        user_input = self.entry.get()
        if self.validate_sentence(user_input, self.current_sentence["rule"]):
            self.score += 10
            self.feedback_label.config(text="Correct! ✔️", fg="green")
            self.update_score()
            self.next_sentence()
        else:
            self.score -= 5
            self.feedback_label.config(text="Wrong! ❌", fg="red")
            self.update_score()
            self.root.after(1000, self.next_sentence)

    def validate_sentence(self, sentence, rule):
        if rule == "a*b*":
            return bool(re.match(r'^a*b*$', sentence))
        elif rule == "balanced_parentheses":
            stack = []
            for char in sentence:
                if char == '(':
                    stack.append(char)
                elif char == ')':
                    if not stack:
                        return False
                    stack.pop()
            return not stack
        elif rule == "palindrome":
            return sentence == sentence[::-1]
        elif rule == "alternating_01":
            return bool(re.match(r'^(01)*$', sentence))
        elif rule == "contains_101":
            return bool(re.search(r'101', sentence))
        elif rule == "ends_in_01":
            return bool(re.match(r'^(0|1)*01$', sentence))
        elif rule == "a+b+c":
            return bool(re.match(r'^[a]+[b]+[c]+$', sentence))
        elif rule == "a*b*c":
            return bool(re.match(r'^[a]*[b]*[c]*$', sentence))
        elif rule == "a*b+c":
            return bool(re.match(r'^[a]*[b]+[c]+$', sentence))
        return False

    def skip_sentence(self):
        self.next_sentence()

    def end_game(self):
        self.sentence_label.config(text="Time's up!")
        self.entry.config(state=tk.DISABLED)
        self.start_button.config(text="Restart Game", command=self.reset_game)
        self.skip_button.pack_forget()  # Hide skip button when game ends

    def reset_game(self):
        self.entry.config(state=tk.NORMAL)
        self.start_button.config(text="Start Game", command=self.start_game)
        self.update_score()
        self.update_timer()

root = tk.Tk()
game = TypingGame(root)
root.mainloop()


