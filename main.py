import tkinter as tk
from game.ui import TypingGame

if __name__ == '__main__':
    root = tk.Tk()
    root.minsize(480, 430)
    TypingGame(root)
    root.mainloop()
