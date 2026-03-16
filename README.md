# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game purpose:**
A number guessing game where the player picks a difficulty, then tries to guess a randomly generated secret number within a limited number of attempts. Each guess receives a "Too High" or "Too Low" hint, and the score increases on a win (penalized per attempt) or decreases on wrong guesses.

**Bugs found:**

| # | Location | Bug |
|---|----------|-----|
| 1 | `app.py` — `OUTCOME_HINTS` | Hints were inverted: "Too High" showed "Go HIGHER!" and vice versa |
| 2 | `app.py` — new game reset block | `score` and `history` were never cleared; `attempts` started at `1` instead of `0` |
| 3 | `logic_utils.py` — `get_range_for_difficulty` | Hard difficulty returned range `(1, 50)`, making it easier than Normal `(1, 100)` |
| 4 | `logic_utils.py` — `update_score` | "Too High" on even-numbered attempts awarded `+5` points (wrong guess rewarded the player) |
| 5 | `logic_utils.py` — `update_score` | Win formula used `attempt_number + 1`, double-penalizing score (first-guess win gave 80 pts instead of 90) |

**Fixes applied:**

1. Swapped the hint strings in `OUTCOME_HINTS` so `"Too High"` maps to `"Go LOWER!"` and `"Too Low"` maps to `"Go HIGHER!"`.
2. Added `st.session_state.score = 0` and `st.session_state.history = []` to the new-game reset block; changed `attempts` initialization from `1` to `0` in both the initial state and the reset.
3. Changed Hard difficulty range from `(1, 50)` to `(1, 500)`.
4. Removed the even/odd attempt branching in `update_score` — "Too High" now always returns `current_score - 5`, consistent with "Too Low".
5. Removed the `+ 1` from the win score formula: `100 - 10 * attempt_number`.
6. Refactored `attempt_limit_map` out of `app.py` into a new `get_attempt_limit_for_difficulty()` function in `logic_utils.py` so all game rules are testable independently of the UI.

