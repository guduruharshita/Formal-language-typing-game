# Formal Language Typing Game

A Python-based typing game built with Tkinter that tests your understanding of formal language theory concepts. Players must identify and type strings that match specific language rules within a time limit.

## 🎮 Game Overview

This educational game challenges players to recognize patterns in formal languages including:
- Regular expressions (a*b*, a+b+c, a*b*c, etc.)
- Balanced parentheses
- Palindromes
- Binary patterns (alternating, containing specific substrings)

## ✨ Features

- **9 Different Language Rules**: Various patterns to test your formal language knowledge
- **Scoring System**: +10 points for correct answers, -5 for wrong answers
- **45-Second Timer**: Race against time to identify as many patterns as possible
- **Skip Option**: Skip difficult sentences if needed
- **Visual Feedback**: Clear indication of correct/incorrect answers
- **Restart Capability**: Play multiple rounds

## 📋 Language Rules Included

| Rule | Description | Example |
|------|-------------|---------|
| `a*b*` | Zero or more 'a's followed by zero or more 'b's | `aaaabbbb` |
| `balanced_parentheses` | Properly nested parentheses | `(())` |
| `palindrome` | Reads the same forwards and backwards | `racecar` |
| `alternating_01` | Alternating 0s and 1s | `01` |
| `contains_101` | Contains substring '101' | `00101` |
| `ends_in_01` | Ends with '01' | `01101` |
| `a+b+c` | One or more 'a's, then one or more 'b's, then one or more 'c's | `aaabbbccc` |
| `a*b*c` | Zero or more 'a's, then zero or more 'b's, then zero or more 'c's | `aabbbccc` |
| `a*b+c` | Zero or more 'a's, then one or more 'b's, then one or more 'c's | `aaabccc` |

## 🛠️ Requirements

- Python 3.x
- Tkinter (included with standard Python installations)

## 🚀 How to Run

1. Make sure you have Python installed
2. Clone this repository or download the files
3. Run the game:
   ```bash
   python "Toc final.py"
   ```

## 🎯 How to Play

1. Click **"Start Game"** to begin
2. A sentence will appear on the screen
3. Type the corresponding language rule (e.g., `a*b*`, `palindrome`, `balanced_parentheses`)
4. Press **Enter** to submit your answer
5. Score as many points as possible before time runs out!

## 📁 Project Structure

```
Toc/
├── Toc final.py          # Main game file
├── README.md             # This file
└── Formal Language Typing Game.pdf  # Project documentation
```

## 🧠 Educational Value

This game helps students learn and practice:
- Regular expressions
- Formal language theory
- Pattern recognition
- String manipulation concepts

## 📝 License

This project is available for educational purposes.

---

*Created as a learning project for Formal Language Theory*

