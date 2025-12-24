import tkinter as tk
from game.ui import TypingGame

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(500, 450)
    TypingGame(root)
    root.mainloop()
