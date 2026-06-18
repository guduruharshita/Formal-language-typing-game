"""Challenge definitions grouped by formal language class and difficulty."""

from dataclasses import dataclass
from enum import StrEnum


class Difficulty(StrEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Category(StrEnum):
    REGULAR = "Regular Language"
    CONTEXT_FREE = "Context-Free Language"
    STRING_PROPERTY = "String Property"


@dataclass(frozen=True)
class Challenge:
    rule: str
    label: str
    description: str
    hint: str
    example: str
    category: Category
    difficulty: Difficulty
    points: int


CHALLENGES: list[Challenge] = [
    # ── Easy Regular ──────────────────────────────────────────────────────────
    Challenge(
        rule="a_star_b_star",
        label="a*b*",
        description="Zero or more a's followed by zero or more b's.",
        hint="Try: aaabbb, aab, bb, or even the empty string",
        example="aaabbb",
        category=Category.REGULAR,
        difficulty=Difficulty.EASY,
        points=10,
    ),
    Challenge(
        rule="alternating_01",
        label="(01)*",
        description="Repeated pairs of '01' — zero or more repetitions.",
        hint="Each pair must be exactly '01'. Try: 01, 0101, 010101",
        example="0101",
        category=Category.REGULAR,
        difficulty=Difficulty.EASY,
        points=10,
    ),
    Challenge(
        rule="only_a_or_b",
        label="[ab]+",
        description="One or more characters, each of which is 'a' or 'b'.",
        hint="Any non-empty string using only 'a' and 'b'",
        example="ababba",
        category=Category.REGULAR,
        difficulty=Difficulty.EASY,
        points=10,
    ),
    Challenge(
        rule="ends_in_01",
        label="[01]*01",
        description="A binary string that ends with '01'.",
        hint="The last two characters must be '01'",
        example="11001",
        category=Category.REGULAR,
        difficulty=Difficulty.EASY,
        points=10,
    ),
    # ── Medium Regular ────────────────────────────────────────────────────────
    Challenge(
        rule="a_plus_b_plus_c_plus",
        label="a+b+c+",
        description="One or more a's, then one or more b's, then one or more c's.",
        hint="Must have at least one of each: 'abc', 'aabbc', 'aaabbbccc'",
        example="aaabbbccc",
        category=Category.REGULAR,
        difficulty=Difficulty.MEDIUM,
        points=15,
    ),
    Challenge(
        rule="contains_101",
        label="∃ substring '101'",
        description="Any binary string that contains '101' as a substring.",
        hint="'101' must appear somewhere. Try: 101, 0101, 11011",
        example="11011",
        category=Category.REGULAR,
        difficulty=Difficulty.MEDIUM,
        points=15,
    ),
    Challenge(
        rule="even_length_binary",
        label="even-length {0,1}+",
        description="A non-empty binary string of even length.",
        hint="Length must be 2, 4, 6, … Try: 00, 1010, 1100",
        example="1010",
        category=Category.REGULAR,
        difficulty=Difficulty.MEDIUM,
        points=15,
    ),
    Challenge(
        rule="starts_ends_same",
        label="starts & ends with same char",
        description="String of length ≥ 2 where first and last characters are equal.",
        hint="First char == last char. Try: aba, abba, 1001",
        example="abcba",
        category=Category.REGULAR,
        difficulty=Difficulty.MEDIUM,
        points=15,
    ),
    Challenge(
        rule="divisible_3_unary",
        label="1^(3k)",
        description="Unary string of 1s whose length is a multiple of 3.",
        hint="Length must be 0, 3, 6, 9, … Try: 111, 111111",
        example="111111",
        category=Category.REGULAR,
        difficulty=Difficulty.MEDIUM,
        points=15,
    ),
    # ── Hard Regular ──────────────────────────────────────────────────────────
    Challenge(
        rule="binary_even_ones",
        label="even number of 1s",
        description="A non-empty binary string containing an even count of 1-bits.",
        hint="Count the 1s — must be 0, 2, 4, … Try: 00, 110, 1001",
        example="1100",
        category=Category.REGULAR,
        difficulty=Difficulty.HARD,
        points=20,
    ),
    Challenge(
        rule="a_star_b_star_c_star",
        label="a*b*c*",
        description="Zero or more a's, then b's, then c's (all optional, order fixed).",
        hint="Can be empty. Each section optional but order is fixed: a before b before c",
        example="aabbc",
        category=Category.REGULAR,
        difficulty=Difficulty.HARD,
        points=20,
    ),
    # ── Context-Free ─────────────────────────────────────────────────────────
    Challenge(
        rule="balanced_parens",
        label="Balanced Parentheses",
        description="A string of parentheses where every '(' is matched by a closing ')'.",
        hint="Count opening parens — all must close. Try: (), (()), ()(), (()())",
        example="(()())",
        category=Category.CONTEXT_FREE,
        difficulty=Difficulty.EASY,
        points=10,
    ),
    Challenge(
        rule="palindrome",
        label="Palindrome",
        description="A non-empty string that reads the same forwards and backwards.",
        hint="Try: aba, racecar, abcba, 1001",
        example="racecar",
        category=Category.CONTEXT_FREE,
        difficulty=Difficulty.EASY,
        points=10,
    ),
    Challenge(
        rule="n_a_n_b",
        label="aⁿbⁿ  (n ≥ 1)",
        description="Exactly n a's followed by exactly n b's for some n ≥ 1.",
        hint="Count must match: 'ab', 'aabb', 'aaabbb'",
        example="aaabbb",
        category=Category.CONTEXT_FREE,
        difficulty=Difficulty.MEDIUM,
        points=15,
    ),
    Challenge(
        rule="equal_ab",
        label="equal #a and #b",
        description="A non-empty string over {a, b} with equal counts of a and b.",
        hint="#a == #b. Try: ab, ba, aabb, abba, abab",
        example="aababb",
        category=Category.CONTEXT_FREE,
        difficulty=Difficulty.MEDIUM,
        points=15,
    ),
    Challenge(
        rule="ww_reverse",
        label="w·wᴿ",
        description="A string of even length that is the concatenation of w and its reverse.",
        hint="First half mirrors second half in reverse. Try: abba, abccba, 1001",
        example="abccba",
        category=Category.CONTEXT_FREE,
        difficulty=Difficulty.HARD,
        points=20,
    ),
    Challenge(
        rule="n_a_m_b_n_c",
        label="aⁿbᵐcⁿ  (n ≥ 1)",
        description="n a's, then zero or more b's, then exactly n c's.",
        hint="#a must equal #c. b's in the middle are optional. Try: ac, abc, aabcc, aabbbcc",
        example="aabbbcc",
        category=Category.CONTEXT_FREE,
        difficulty=Difficulty.HARD,
        points=20,
    ),
    # ── String Properties ─────────────────────────────────────────────────────
    Challenge(
        rule="no_consecutive",
        label="no consecutive identical chars",
        description="A non-empty string where no two adjacent characters are the same.",
        hint="abab, aba, 0101, abcabc — never 'aa' or '11'",
        example="ababab",
        category=Category.STRING_PROPERTY,
        difficulty=Difficulty.MEDIUM,
        points=15,
    ),
    Challenge(
        rule="three_consecutive",
        label="contains 3 consecutive identical chars",
        description="A string containing at least three identical characters in a row.",
        hint="Examples: aaa, 111, abbbba, aaab",
        example="aaabbc",
        category=Category.STRING_PROPERTY,
        difficulty=Difficulty.MEDIUM,
        points=15,
    ),
    Challenge(
        rule="alternating_ab",
        label="(ab)+ or (ba)+",
        description="A string that is one or more repetitions of 'ab' or one or more of 'ba'.",
        hint="abab, ab, baba, ba — must be pure (ab)* or (ba)*",
        example="ababab",
        category=Category.STRING_PROPERTY,
        difficulty=Difficulty.HARD,
        points=20,
    ),
]

# Index by rule name for O(1) lookup
CHALLENGE_MAP: dict[str, Challenge] = {c.rule: c for c in CHALLENGES}
