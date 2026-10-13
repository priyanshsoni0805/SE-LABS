# Lab 4: VibeCoding: AI Usage Record

| | |
|---|---|
| **Student** | Priyansh Soni |
| **Project** | `36_dinoRun` (Pygame endless runner) |
| **Personal repository** | https://github.com/priyanshsoni0805/36_dinorun |
| **AI tool used** | ChatGPT |
| **Full chat link** | `<PASTE YOUR CHATGPT "SHARE" LINK HERE>` |

> **Note on this document:** This is a structured summary of how I used ChatGPT
> for Lab 4. It is not a word-for-word transcript. The complete, unedited
> conversation is available at the share link above (README requires the
> "Chat/LLM used page link with the complete chat history").

---

## 1. Starting point

I read the handout and the project README. The game is a single file (`game.py`)
with **one deliberate bug** and **three empty feature hooks**:

| # | Task | Location in `game.py` |
|---|------|----------------------|
| 1 | Fix the high-score bug (comparison was backwards) | `Game.update`, after collision |
| 2 | Implement `dino_tint(on_ground)` | called in `Dino.draw` |
| 3 | Implement `on_obstacle_passed(obstacle, score)` | called in `Game.update` |
| 4 | Implement `max_jumps()` | used in `Dino.jump` |

I recorded a 10-second "before" video, then shared the project and README with ChatGPT.

## 2. Task-by-task: what I asked and what changed

### Task 1: High-score bug
- **Prompt (summary):** Shared the project and README and asked ChatGPT to find why the high score never updates.
- **Diagnosis:** The `if` after the collision compared the values in the wrong order, so a new score could never beat the stored best.
- **Final code:**
  ```python
  current = max(0, self.score // 10)
  if current > self.high_score:
      self.high_score = current
      save_high_score(self.high_score)
  ```
- **My review:** The new score must be on the left (the run that just ended) and the stored best on the right. `save_high_score` writes to `dino_highscore.txt`, and `load_high_score` reads it back on startup.

### Task 2: `dino_tint(on_ground)`
- **Goal:** Different dino colour while airborne.
- **Final code:**
  ```python
  def dino_tint(on_ground):
      return (83, 141, 78) if on_ground else (70, 145, 225)   # green / blue
  ```
- **Result:** Dino is green on the ground and blue mid-jump (confirmed on my Mac).

### Task 3: `on_obstacle_passed(obstacle, score)`
- **Goal:** Visual feedback when an obstacle is cleared.
- **Implementation:** A global `PASS_COMBO` counter increments per obstacle cleared, and a `"+1  COMBO xN"` popup is added to `PASS_POPUPS` above the obstacle (42-frame timer). The combo resets on collision and in `Game.reset()`. The HUD shows `Score / Best / Combo`.

### Task 4: `max_jumps()`
- **Implementation:** `return 2`. The existing `jump_count` logic in `Dino.jump` handles the rest, giving a double jump. The start-screen hint was updated to mention it.
- **Result:** Double jump confirmed working on my Mac.

## 3. Testing and verification
- ChatGPT could not run Pygame in its own environment, so it did not test gameplay itself.
- I ran `python game.py` on my Mac and confirmed: the high score updates and persists, the dino changes colour in the air, double jump works, and the combo popups appear.
- I recorded a 10-second "after" video showing all four changes.

## 4. Git / GitHub issues I worked through
1. **Unmatched quote in `git commit -m "..."`**: Terminal stuck at `dquote>`. Fixed with `Control + C`, then re-ran each Git command separately.
2. **Commit succeeded** (`.DS_Store`, `.gitignore`, `README.md`, `dino_highscore.txt`, `game.py`).
3. **`git push -u origin main` rejected**: GitHub no longer accepts account passwords over HTTPS. Resolved by using a Personal Access Token (or browser sign-in) instead.
4. `<CONFIRM: push succeeded and files are visible on the GitHub page>`

## 5. Reflection
- The bug was found quickly once the README pointed to the exact `if` condition; I still checked the comparison direction myself rather than just pasting the fix.
- Treating each feature as a separate prompt kept the changes small and easy to verify.
- Because the AI could not run the game, my own testing on a real machine was essential.

## 6. Submission checklist
- [ ] Updated code pushed to `priyanshsoni0805/36_dinorun` (no PR to `SETAPESU26`)
- [ ] Before video (10 s)
- [ ] After video (10 s)
- [ ] This document (and the ChatGPT share link) in the `Lab-4` folder
- [ ] Link submitted on Microsoft Teams
