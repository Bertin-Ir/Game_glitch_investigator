def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 500  # FIX: was (1, 50) — AI caught that Hard was easier than Normal; verified via test_get_range_for_difficulty
    return 1, 100


def get_attempt_limit_for_difficulty(difficulty: str) -> int:
    """Return the maximum number of guesses allowed for a given difficulty."""
    limits = {"Easy": 6, "Normal": 8, "Hard": 5}
    return limits.get(difficulty, 8)


def parse_guess(raw: str):
    """Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """Compare guess to secret and return outcome.

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win"

    # Ensure we can compare numbers (raises TypeError if not comparable)
    try:
        if guess > secret:
            return "Too High"
        return "Too Low"
    except TypeError:
        # If types are mismatched, try a string comparison as a fallback
        try:
            g = str(guess)
            s = str(secret)
            if g == s:
                return "Win"
            if g > s:
                return "Too High"
            return "Too Low"
        except Exception:
            return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # FIX: was (attempt_number + 1) — AI found the +1 double-counted since attempts
        # is already incremented before this call; verified by test_update_score_win_first_attempt.
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    # FIX: AI identified that "Too High" on even attempts previously returned +5,
    # rewarding a wrong guess; simplified to always -5 to match "Too Low" behavior.
    # Verified by test_update_score_too_high_even_attempt (expected 5 → corrected to -5).
    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
