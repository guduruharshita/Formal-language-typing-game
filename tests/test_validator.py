from formal_game.validator import validate

# ── Regular Language tests ────────────────────────────────────────────────────

class TestRegular:
    def test_a_star_b_star_valid(self):
        assert validate("a_star_b_star", "aaabbb")
        assert validate("a_star_b_star", "")
        assert validate("a_star_b_star", "aaa")
        assert validate("a_star_b_star", "bbb")

    def test_a_star_b_star_invalid(self):
        assert not validate("a_star_b_star", "bba")
        assert not validate("a_star_b_star", "aba")

    def test_alternating_01_valid(self):
        assert validate("alternating_01", "01")
        assert validate("alternating_01", "0101")
        assert validate("alternating_01", "")

    def test_alternating_01_invalid(self):
        assert not validate("alternating_01", "10")
        assert not validate("alternating_01", "0")
        assert not validate("alternating_01", "011")

    def test_ends_in_01(self):
        assert validate("ends_in_01", "01")
        assert validate("ends_in_01", "11001")
        assert not validate("ends_in_01", "10")
        assert not validate("ends_in_01", "100")

    def test_contains_101(self):
        assert validate("contains_101", "101")
        assert validate("contains_101", "0101")
        assert not validate("contains_101", "100")
        assert not validate("contains_101", "010")

    def test_even_length_binary(self):
        assert validate("even_length_binary", "00")
        assert validate("even_length_binary", "1010")
        assert not validate("even_length_binary", "101")
        assert not validate("even_length_binary", "")

    def test_divisible_3_unary(self):
        assert validate("divisible_3_unary", "")
        assert validate("divisible_3_unary", "111")
        assert validate("divisible_3_unary", "111111")
        assert not validate("divisible_3_unary", "1")
        assert not validate("divisible_3_unary", "11")

    def test_binary_even_ones(self):
        assert validate("binary_even_ones", "00")   # 0 ones = even
        assert validate("binary_even_ones", "11")   # 2 ones = even
        assert validate("binary_even_ones", "1001") # 2 ones = even
        assert validate("binary_even_ones", "101")  # 2 ones = even
        assert not validate("binary_even_ones", "1")    # 1 one = odd
        assert not validate("binary_even_ones", "1011") # 3 ones = odd


# ── Context-Free tests ────────────────────────────────────────────────────────

class TestContextFree:
    def test_balanced_parens_valid(self):
        assert validate("balanced_parens", "()")
        assert validate("balanced_parens", "(())")
        assert validate("balanced_parens", "()()")
        assert validate("balanced_parens", "")

    def test_balanced_parens_invalid(self):
        assert not validate("balanced_parens", "(")
        assert not validate("balanced_parens", ")")
        assert not validate("balanced_parens", ")(")
        assert not validate("balanced_parens", "(()")

    def test_palindrome(self):
        assert validate("palindrome", "a")
        assert validate("palindrome", "racecar")
        assert validate("palindrome", "aba")
        assert validate("palindrome", "1001")
        assert not validate("palindrome", "ab")
        assert not validate("palindrome", "abc")

    def test_n_a_n_b(self):
        assert validate("n_a_n_b", "ab")
        assert validate("n_a_n_b", "aabb")
        assert validate("n_a_n_b", "aaabbb")
        assert not validate("n_a_n_b", "aab")
        assert not validate("n_a_n_b", "abb")
        assert not validate("n_a_n_b", "b")

    def test_equal_ab(self):
        assert validate("equal_ab", "ab")
        assert validate("equal_ab", "ba")
        assert validate("equal_ab", "aabb")
        assert validate("equal_ab", "abba")
        assert not validate("equal_ab", "a")
        assert not validate("equal_ab", "aab")

    def test_ww_reverse(self):
        assert validate("ww_reverse", "abba")
        assert validate("ww_reverse", "abccba")
        assert validate("ww_reverse", "1001")
        assert not validate("ww_reverse", "abc")
        assert not validate("ww_reverse", "abcd")
        assert not validate("ww_reverse", "a")

    def test_n_a_m_b_n_c(self):
        assert validate("n_a_m_b_n_c", "ac")
        assert validate("n_a_m_b_n_c", "abc")
        assert validate("n_a_m_b_n_c", "aabcc")
        assert validate("n_a_m_b_n_c", "aabbbcc")
        assert not validate("n_a_m_b_n_c", "aabc")
        assert not validate("n_a_m_b_n_c", "b")


# ── String Property tests ─────────────────────────────────────────────────────

class TestStringProperties:
    def test_no_consecutive(self):
        assert validate("no_consecutive", "ab")
        assert validate("no_consecutive", "aba")
        assert validate("no_consecutive", "abab")
        assert not validate("no_consecutive", "aa")
        assert not validate("no_consecutive", "abb")

    def test_three_consecutive(self):
        assert validate("three_consecutive", "aaa")
        assert validate("three_consecutive", "aaab")
        assert validate("three_consecutive", "111")
        assert not validate("three_consecutive", "aa")
        assert not validate("three_consecutive", "aba")

    def test_alternating_ab(self):
        assert validate("alternating_ab", "ab")
        assert validate("alternating_ab", "abab")
        assert validate("alternating_ab", "ba")
        assert validate("alternating_ab", "baba")
        assert not validate("alternating_ab", "a")
        assert not validate("alternating_ab", "aba")
        assert not validate("alternating_ab", "abba")


# ── Unknown rule ──────────────────────────────────────────────────────────────

def test_unknown_rule_returns_false():
    assert not validate("no_such_rule", "anything")
