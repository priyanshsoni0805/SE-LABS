# Lab 4: Vibe Coding — Dino Run Repair Lab

**Name:** Priyansh Soni  **SRN:** PES1UG24CS344
**Project:** `36_dinoRun` (single-file Pygame endless runner)  **Personal repo:** https://github.com/priyanshsoni0805/36_dinorun
**AI assistant used:** ChatGPT

Dino Run is a side-scrolling endless runner. The dino jumps over randomly sized obstacles that spawn at random intervals and speed up as the score climbs. The starter code had **one deliberate bug** (the high score never updated) and **three empty feature hooks**. I fixed the bug and implemented the three hooks with ChatGPT as a pair-programming partner, one task at a time, and checked each result myself.

## Submission

| Deliverable | File |
|---|---|
| Updated code | `game.py` |
| 10-second gameplay video **before** changes | `original video.mov` |
| 10-second gameplay video **after** changes | `updated game video.mov` |
| AI usage record and chat history | `Lab4_AI_Chat_History_.md` |
| High-score file written by the game | `dino_highscore.txt` |

## Folder structure

```
PES1UG24CS344_LAB4/
├── README.md
├── game.py
├── dino_highscore.txt
├── Lab4_AI_Chat_History_.md
├── original video.mov
└── updated game video.mov
```

## How to run

Requires Python 3.10+ and Pygame.

```bash
pip install pygame
python game.py
```

**Controls:** `Space`, `Up` or `W` starts the game, jumps (twice in the air, see Task 4), and restarts after Game Over. Closing the window quits.

## What was fixed or added

| # | Task | Where in `game.py` | What I did |
|---|------|--------------------|------------|
| 1 | Fix the high-score bug | `Game.update`, right after a collision | The comparison was backwards, so a run could never beat the stored best. The run that just ended is now on the left: `if current > self.high_score:`, and then the new best is stored and saved. |
| 2 | `dino_tint(on_ground)` | called in `Dino.draw` | Returns green `(83, 141, 78)` on the ground and blue `(70, 145, 225)` while airborne. |
| 3 | `on_obstacle_passed(obstacle, score)` | called in `Game.update` | Keeps a consecutive-clear combo (`PASS_COMBO`) and spawns a floating `+1  COMBO xN` popup above the cleared obstacle for 42 frames. The HUD shows `Score / Best / Combo`. |
| 4 | `max_jumps()` | used in `Dino.jump` | Returns `2`, giving a double jump. The existing `jump_count` logic resets on landing. The start-screen hint now mentions the double jump. |

### Task 1 in detail

```python
current = max(0, self.score // 10)
if current > self.high_score:      # run that just ended vs best so far
    self.high_score = current
    save_high_score(self.high_score)
```

`load_high_score()` reads `dino_highscore.txt` on startup, and returns `0` if the file is missing or unreadable. `save_high_score()` writes it, and the game still plays if the folder is read-only.

### Task 3 in detail

- The combo increments once per obstacle, the first frame its right edge passes the dino's left edge (`obs.passed` stops double counting).
- A collision resets the combo to 0, and `Game.reset()` clears both the combo and the popup list, so a restart starts clean.

## Testing

**Manual:** I played the game on my Mac and confirmed that the high score updates and survives a restart, the dino changes colour in the air, double jump works, and the combo popups appear. The "after" video shows all four changes.

**Logic checks:** I also exercised the game logic in a script with Pygame replaced by a minimal stub, so no window was opened.

| Check | Result |
|---|---|
| Best score loaded from `dino_highscore.txt` on start | Pass |
| Crash with score 100 (stored best 5) | Best becomes 100 and the file contains `100` |
| Crash with a lower score afterwards | Best and file stay at 100 |
| Three jump presses in a row | `jump_count` stops at 2 |
| Landing | `jump_count` back to 0 |
| `dino_tint(True)` / `dino_tint(False)` | Green / blue |
| Passing an obstacle | Combo 1 and one popup created |

## Known limitations

- **The high score is saved only when the dino crashes.** Closing the window mid-run does not save it.
- **Speed-up only affects new obstacles.** Each obstacle takes the speed it had when it spawned, so a speed increase applies from the next spawn onward.
- `dino_tint` never returns `None`, so the `or self.color` fallback in `Dino.draw` is never used.
- `PASS_COMBO` and `PASS_POPUPS` are module-level globals, which keeps the hook signatures from the starter code but is not ideal design.
- The two videos are each about 17 seconds long, while the handout asks for 10-second videos.
- `Lab4_AI_Chat_History_.md` is a structured summary, not a word-for-word transcript. The complete conversation is the ChatGPT share link, which still has to be pasted into that file.

## AI usage

I used ChatGPT as a debugging partner. I shared the project and handout, asked it to find why the high score never updated, then handled each feature as a separate prompt so every change stayed small and easy to check. ChatGPT could not run Pygame, so all gameplay testing was done by me. Prompts, diagnoses, final code and the Git problems I ran into are recorded in `Lab4_AI_Chat_History_.md`.
