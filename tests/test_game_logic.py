import os
import sys

# Ensure the project root is on sys.path so imports work regardless of pytest root discovery.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from logic_utils import (
    check_guess,
    get_attempt_limit_for_difficulty,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


def test_parse_guess_invalid():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_guess_non_numeric():
    ok, value, err = parse_guess("hello")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_guess_float_string():
    ok, value, err = parse_guess("42.9")
    assert ok is True
    assert value == 42
    assert err is None


def test_get_range_for_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 500)
    assert get_range_for_difficulty("Unknown") == (1, 100)


def test_get_attempt_limit_for_difficulty():
    assert get_attempt_limit_for_difficulty("Easy") == 6
    assert get_attempt_limit_for_difficulty("Normal") == 8
    assert get_attempt_limit_for_difficulty("Hard") == 5
    assert get_attempt_limit_for_difficulty("Unknown") == 8


def test_update_score_win_minimum_points():
    # If the player wins late, it should still award at least 10 points
    score = update_score(0, "Win", 20)
    assert score == 10


def test_update_score_win_first_attempt():
    # Winning on the first guess should award 90 points (100 - 10*1).
    # Regression: a prior bug used (attempt_number + 1), which gave 80 instead.
    score = update_score(0, "Win", 1)
    assert score == 90


def test_update_score_too_high_even_attempt():
    assert update_score(0, "Too High", 2) == -5


def test_update_score_too_high_odd_attempt():
    assert update_score(0, "Too High", 3) == -5


def test_update_score_too_low():
    assert update_score(0, "Too Low", 1) == -5
