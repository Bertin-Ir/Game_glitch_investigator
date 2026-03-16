# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").


Here are at least three concrete bugs I identified:

1. Hints are wrong (higher/lower messages inverted)
When your guess is too high, the game says “Go HIGHER!”
When your guess is too low, the game says “Go LOWER!”

2. New Game doesn’t fully reset the game state.
You can start a “new game” but still be stuck saying “Game over” or carry over scores/guesses from the last round.

3. Incorrect attempt counter initialization: The game started with attempts = 1 instead of 0, causing the "attempts left" display to be off by one. For example, with 8 attempts allowed on Normal difficulty, it showed 7 attempts left at the start instead of 8, making it confusing for players to track their remaining guesses.

4. Secret number appears to change when submitting guesses, because the code mixes types (int vs str) in comparisons and produces inconsistent results even though the secret value is actually stable.

## 2. How did you use AI as a teammate?

I used **Claude Code**  as my primary AI collaborator throughout this project, working in an agentic mode where it could read files, propose fixes, and run tests. I also used chatgpt to refine my prompt, as well github copilot to plan, and suggest fixes

**Correct AI suggestion — "Too High" scoring bug:**
github copilot scanned `logic_utils.py` and flagged that `update_score` returned `+5` points for a "Too High" guess on even-numbered attempts. It correctly identified this as a logic error: a wrong answer should never reward the player. It traced the asymmetry against the "Too Low" branch (which always returned `-5`) and suggested collapsing both wrong-answer cases to a flat `-5`. I verified this by updating `test_update_score_too_high_even_attempt` to expect `-5` and running `pytest` — all 13 tests passed. I also cross-checked by reading the scoring section of `logic_utils.py` and confirming the even/odd branching was gone.

**Incorrect / misleading AI suggestion — "Attempts left" display:**
During the audit, Claude Code flagged the line `attempt_limit - st.session_state.attempts` (app.py line 56) as a potential off-by-one error, suggesting it could display negative numbers in edge cases. After tracing the Streamlit execution model — the full script reruns top-to-bottom on every interaction, so the display always reflects the post-increment value from the *previous* run — I determined the display was actually correct. The AI's suggestion was misleading because it didn't fully account for Streamlit's rerun model: the counter shown before the submit button is always one run behind the current click, which is exactly the right value to show. I verified by running the app, stepping through several guesses on Easy difficulty (6 attempts), and confirming the "Attempts left" counter decreased correctly from 6 → 5 → 4 without going negative.

---

## 3. Debugging and testing your fixes

I used a two-pronged approach: `pytest` for logic verification and the live Streamlit app for UI/state verification.

**pytest — win score formula regression:**
After Claude Code fixed the win formula from `100 - 10 * (attempt_number + 1)` to `100 - 10 * attempt_number`, I added `test_update_score_win_first_attempt` which calls `update_score(0, "Win", 1)` and asserts `== 90`. The existing test (`test_update_score_win_minimum_points`) used attempt 20, where the result clamps to 10 either way — it was blind to the bug. The new test would return `80` with the old formula and `90` with the fix, confirming the formula was corrected. Running `pytest -v` showed all 13 tests green.

**Manual Streamlit testing — new game state reset:**
I verified the new-game reset fix by running `python -m streamlit run app.py`, playing a full game to completion (win or loss), then clicking "New Game." I opened the Developer Debug Info expander and confirmed `score: 0`, `attempts: 0`, and `history: []` before making any new guess. Previously, the score and history carried over from the previous round, which was visible in that same expander.

**pytest full suite as a safety net:**
After every individual fix, I ran the full `pytest` suite to ensure nothing regressed. This caught the test file itself needing updates (e.g., `test_update_score_too_high_even_attempt` still expected `5` after the scoring fix was applied to `logic_utils.py`), which Claude Code flagged and corrected in the same pass.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit reruns the entire Python script from top to bottom every time a user interacts with the app, such as clicking a button or changing input. This full-rerun model means the UI reflects the state after the previous interaction, which can be confusing at first but ensures consistency. Session state acts like a persistent save file, storing variables like the secret number across reruns so they don't reset. To explain to a friend: think of it as a choose-your-own-adventure book where every choice flips back to page one, but your bookmarks (session state) remember where you left off, allowing the story to continue coherently.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to reuse is separating UI code from business logic into testable pure functions, like moving game rules to logic_utils.py, which made bugs easier to isolate and verify with unit tests. Next time with AI, I would verify suggestions by understanding the framework's mechanics first, rather than just testing, to avoid accepting misleading advice like the "attempts left" off-by-one claim. This project changed my thinking about AI-generated code by showing that even intentionally buggy code teaches deeper understanding, shifting from blind trust to critical verification and learning why bugs occur.
