import re

def validate(sentence: str, rule: str) -> bool:
    rules = {
        "a_star_b_star":        lambda s: bool(re.fullmatch(r'a*b*', s)),
        "balanced_parens":      _balanced_parens,
        "palindrome":           lambda s: s == s[::-1],
        "alternating_01":       lambda s: bool(re.fullmatch(r'(01)*', s)),
        "contains_101":         lambda s: bool(re.search(r'101', s)),
        "ends_in_01":           lambda s: bool(re.fullmatch(r'[01]*01', s)),
        "a_plus_b_plus_c_plus": lambda s: bool(re.fullmatch(r'a+b+c+', s)),
        "a_star_b_star_c":      lambda s: bool(re.fullmatch(r'a*b*c*', s)),
        "a_star_b_plus_c":      lambda s: bool(re.fullmatch(r'a*b+c+', s)),
    }
    fn = rules.get(rule)
    return fn(sentence) if fn else False

def _balanced_parens(s: str) -> bool:
    stack = []
    for ch in s:
        if ch == '(':
            stack.append(ch)
        elif ch == ')':
            if not stack:
                return False
            stack.pop()
    return not stack
