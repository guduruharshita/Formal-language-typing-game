# Formal Language Typing Game

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat)](LICENSE)

A Tkinter desktop game that teaches formal language theory through interactive typing challenges. Players type strings that satisfy regular expression rules and formal language patterns under a countdown timer.

## What It Does

Each round displays a string and its formal language rule (e.g. `a*b*`, balanced parentheses, palindrome). The player types a string that satisfies the rule — correct answers score +10, wrong answers lose 5. Nine distinct rules covering regular expressions, context-free patterns, and string properties.

## Rules Covered

| Rule | Pattern | Example |
|------|---------|---------|
| `a*b*` | Zero or more a's followed by b's | `aaaabbbb` |
| Balanced Parentheses | Matched open/close pairs | `(())` |
| Palindrome | Reads same forwards and backwards | `racecar` |
| `(01)*` | Alternating 0 and 1 | `0101` |
| Contains 101 | Substring match | `00101` |
| Ends in 01 | Suffix match | `01101` |
| `a+b+c+` | One or more of each | `aaabbbccc` |

## Project Structure

```
├── game/
│   ├── __init__.py
│   ├── sentences.py    # Challenge data
│   ├── validator.py    # Formal language validation engine
│   └── ui.py           # Tkinter game UI
├── main.py
└── requirements.txt
```

## How to Run

```bash
python main.py
```

No external dependencies — uses Python's standard `tkinter` library only.

## Scoring

- **+10** correct answer
- **-5** wrong answer (minimum 0)
- **45 seconds** per game

## Author

**Harshita Guduru** — [GitHub](https://github.com/guduruharshita) · [LinkedIn](https://linkedin.com/in/harshita-guduru)
