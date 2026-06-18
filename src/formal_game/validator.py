"""Formal language validation functions for each challenge rule."""

import re


def validate(rule: str, s: str) -> bool:
    """Return True if string s satisfies the given formal language rule."""
    fn = _RULES.get(rule)
    return fn(s) if fn is not None else False


# ── Regular Languages ────────────────────────────────────────────────────────

def _a_star_b_star(s: str) -> bool:
    return bool(re.fullmatch(r"a*b*", s))


def _alternating_01(s: str) -> bool:
    return bool(re.fullmatch(r"(01)*", s))


def _ends_in_01(s: str) -> bool:
    return bool(re.fullmatch(r"[01]*01", s))


def _a_plus_b_plus_c_plus(s: str) -> bool:
    return bool(re.fullmatch(r"a+b+c+", s))


def _a_star_b_star_c_star(s: str) -> bool:
    return bool(re.fullmatch(r"a*b*c*", s))


def _a_star_b_plus_c_plus(s: str) -> bool:
    return bool(re.fullmatch(r"a*b+c+", s))


def _contains_101(s: str) -> bool:
    return bool(re.search(r"101", s))


def _even_length_binary(s: str) -> bool:
    return bool(re.fullmatch(r"[01]+", s)) and len(s) % 2 == 0


def _starts_and_ends_same(s: str) -> bool:
    return len(s) >= 2 and s[0] == s[-1]


def _only_a_or_b(s: str) -> bool:
    return bool(re.fullmatch(r"[ab]+", s))


def _divisible_by_3_unary(s: str) -> bool:
    """Unary notation: string of 1s whose length is divisible by 3."""
    return bool(re.fullmatch(r"1*", s)) and len(s) % 3 == 0


def _binary_even_ones(s: str) -> bool:
    """Binary string with an even number of 1-bits."""
    return bool(re.fullmatch(r"[01]+", s)) and s.count("1") % 2 == 0


# ── Context-Free Languages ───────────────────────────────────────────────────

def _balanced_parens(s: str) -> bool:
    depth = 0
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            if depth == 0:
                return False
            depth -= 1
    return depth == 0


def _palindrome(s: str) -> bool:
    return len(s) >= 1 and s == s[::-1]


def _equal_ab(s: str) -> bool:
    """String over {a, b} with equal numbers of a's and b's."""
    return bool(re.fullmatch(r"[ab]+", s)) and s.count("a") == s.count("b")


def _n_a_n_b(s: str) -> bool:
    """Strings of the form a^n b^n (n >= 1)."""
    m = re.fullmatch(r"(a+)(b+)", s)
    return m is not None and len(m.group(1)) == len(m.group(2))


def _n_a_m_b_n_c(s: str) -> bool:
    """Strings of the form a^n b^m c^n (n >= 1, m >= 0)."""
    m = re.fullmatch(r"(a+)(b*)(c+)", s)
    return m is not None and len(m.group(1)) == len(m.group(3))


def _ww_reverse(s: str) -> bool:
    """Strings of the form w w^R where w is any non-empty string (even palindromes)."""
    if len(s) < 2 or len(s) % 2 != 0:
        return False
    half = len(s) // 2
    return s[:half] == s[half:][::-1]


# ── String Properties ────────────────────────────────────────────────────────

def _three_consecutive_same(s: str) -> bool:
    return bool(re.search(r"(.)\1\1", s))


def _no_two_consecutive_same(s: str) -> bool:
    return len(s) >= 1 and not re.search(r"(.)\1", s)


def _alternating_ab(s: str) -> bool:
    return bool(re.fullmatch(r"(ab)+|(ba)+", s))


_RULES: dict[str, object] = {
    # Regular
    "a_star_b_star":       _a_star_b_star,
    "alternating_01":      _alternating_01,
    "ends_in_01":          _ends_in_01,
    "a_plus_b_plus_c_plus": _a_plus_b_plus_c_plus,
    "a_star_b_star_c_star": _a_star_b_star_c_star,
    "a_star_b_plus_c_plus": _a_star_b_plus_c_plus,
    "contains_101":        _contains_101,
    "even_length_binary":  _even_length_binary,
    "starts_ends_same":    _starts_and_ends_same,
    "only_a_or_b":         _only_a_or_b,
    "divisible_3_unary":   _divisible_by_3_unary,
    "binary_even_ones":    _binary_even_ones,
    # Context-Free
    "balanced_parens":     _balanced_parens,
    "palindrome":          _palindrome,
    "equal_ab":            _equal_ab,
    "n_a_n_b":             _n_a_n_b,
    "n_a_m_b_n_c":         _n_a_m_b_n_c,
    "ww_reverse":          _ww_reverse,
    # String Properties
    "three_consecutive":   _three_consecutive_same,
    "no_consecutive":      _no_two_consecutive_same,
    "alternating_ab":      _alternating_ab,
}
