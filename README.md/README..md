# Software Engineering Lab Submissions — PES1UG24CS344

**Name:** Priyansh Soni
**SRN:** PES1UG24CS344

This repository holds my Software Engineering lab work.

- **Labs 1–2** model one system, the **Group Travel Expense Simplification Engine (Problem Statement #37)**: Lab 1 turns it into requirements and a use-case model, and Lab 2 turns those requirements into an Agile backlog and a two-sprint simulation in Jira.
- **Lab 3** is a separate modelling exercise: choosing and justifying an architecture for a **Self-Service Coffee Kiosk System** and drawing its UML component diagram.
- **Lab 4** is a hands-on coding lab: a Pygame endless runner (**Dino Run**) with one bug and three empty feature hooks, repaired with an LLM.
- **Lab 5** applies static code analysis (Pylint, Bandit, Flake8) to a Python **smart-home device controller**.
- **Lab 6** measures and raises code and branch coverage for a Python **highway toll** module.
- **Lab 7** uses Hypothesis fuzz testing to find and fix input-validation bugs in a second highway-toll module.

## Repository Structure

```
.
├── README.md
├── PES1UG24CS344_LAB_1/   Requirements & use-case modelling
│   └── PES1UG24CS344_LAB1_SE.pdf
├── PES1UG24CS344_LAB_2/   Agile backlog & sprint simulation (Jira)
│   └── PES1UG24CS344_LAB2.pdf
├── PES1UG24CS344_LAB3/    Architecture selection & component modelling
│   ├── PES1UG24CS344_Lab3_Justification.pdf
│   └── PES1UG24CS344_Lab3_Component_Diagram.pdf
├── PES1UG24CS344_LAB4/    VibeCoding: Dino Run (Python, Pygame)
│   ├── README.md
│   ├── game.py
│   ├── dino_highscore.txt
│   ├── Lab4_AI_Chat_History_.md
│   ├── original video.mov
│   └── updated game video.mov
├── PES1UG24CS344_LAB5/    Static code analysis: smart home controller (Python)
│   ├── README.md
│   ├── smart_home.py            (cleaned version)
│   ├── smart_home_original.py   (starter code, kept for the "before" reports)
│   ├── issues.md
│   ├── reflection.md
│   ├── run_analysis.sh
│   ├── README_SUBMISSION.md
│   ├── .gitignore
│   └── reports/
│       ├── before/   pylint_report.txt, bandit_report.txt, flake8_report.txt
│       └── after/    pylint_report.txt, bandit_report.txt, flake8_report.txt
├── PES1UG24CS344_LAB6/    Code & branch coverage: highway toll (Python)
│   ├── CodeCoverageTest_PES1UG24CS344_highway_toll.py
│   ├── BranchCoverageTest_PES1UG24CS344_highway_toll.py
│   └── Lab6_Coverage_Report.pdf
└── PES1UG24CS344_LAB7/    Fuzz testing with Hypothesis: highway toll (Python)
    ├── highway_toll.py
    ├── test_highway_toll.py
    └── Lab7_FuzzTesting_Report.pdf
```

## Overview

| Lab | Topic | Deliverables |
|-----|-------|--------------|
| 1 | Requirements table and use-case modelling | Requirements table, UML use-case diagram, use-case flow specification (one PDF) |
| 2 | Agile backlog creation and sprint simulation (Jira) | Backlog, story points, sprint boards, burndown chart, reflection (one PDF) |
| 3 | Architecture selection and component modelling | Written justification, UML component diagram |
| 4 | VibeCoding with an LLM | Fixed and extended `game.py`, before/after videos, AI chat history |
| 5 | Static code analysis (Pylint, Bandit, Flake8) | Cleaned script, issue table, reflection, before/after reports |
| 6 | Code and branch coverage (coverage.py, pytest) | Code coverage tests, branch coverage tests, coverage report |
| 7 | Fuzz testing for input-validation bugs (Hypothesis) | Fixed script, Hypothesis test file, report PDF |

---

## Lab 1 — Requirements & Use-Case Modelling

**System:** Group Travel Expense Simplification Engine (Problem Statement #37)
**Actors:** Group Traveler, Trip Admin

The report (`PES1UG24CS344_LAB1_SE.pdf`) has four parts.

**1. Functional requirements.** Each has a type, priority, acceptance criteria written as pass/fail, and a rationale.

| ID | Priority | Requirement |
|----|----------|-------------|
| FR-001 | High | Record group expenses with payer, amount, currency, date, participants and split details. |
| FR-002 | High | Convert foreign-currency expenses to the trip base currency using the applicable daily exchange rate. |
| FR-003 | High | Calculate each traveler's net balance from all recorded expenses and shares. |
| FR-004 | High | Generate an optimal debt settlement graph that minimizes the number of peer-to-peer payments. |
| FR-005 | Medium | Let travelers and the Trip Admin view the expense ledger, balances and recommended settlement transactions. |

**2. Non-functional requirements.**

| ID | Priority | Requirement |
|----|----------|-------------|
| NFR-001 | High | Performance and security: the settlement engine runs in under 100 ms for groups of up to 50 travelers with 500 expenses, and trip data is protected from unauthorized access. |
| NFR-002 | High | Reliability and data integrity: expense, exchange-rate, balance and settlement data stay consistent, and a failed update never leaves a partially applied transaction. |

**3. UML use-case diagram.** The use cases are *Create / Join Trip*, *Record Expense*, *Convert Currency*, *View Group Balances*, *Manage Trip*, *Calculate Optimal Settlement*, *Calculate Net Balances* and *Settle Debts*. The model includes `«include»` relationships (for example *Record Expense* includes *Convert Currency*) and an `«extend»` relationship.

**4. Use-case flow specification** for *Compute Optimal Debt Settlement*: preconditions, postconditions, an eight-step main success scenario (retrieve expenses and rates, convert currencies, compute net balances, split creditors and debtors, match them with a minimum-transaction strategy, validate that everything settles to zero, display the payments) and an alternate flow for a missing or invalid exchange rate, where the expense is flagged and the calculation pauses until the rate is corrected.

## Lab 2 — Agile Backlog Creation & Sprint Simulation

**Tool:** Jira (backlog, sprint boards and burndown chart)
**Report:** `PES1UG24CS344_LAB2.pdf` (screenshots plus a four-question reflection)

The Lab 1 requirements became three Epics and seven User Stories, estimated by Planning Poker on the Fibonacci scale (three estimators: Alex, Priya and Sam).

| Epic | Story | Priority | Story points |
|------|-------|----------|--------------|
| EPIC-1 Expense & Currency Management | ST-101 Record Group Expense | High | 5 |
| | ST-102 Split Expense Among Participants | High | 3 |
| | ST-103 Convert Foreign Currency | High | 5 |
| EPIC-2 Balance & Debt Settlement | ST-104 Calculate Net Balances | High | 5 |
| | ST-105 Generate Optimal Settlement | High | 8 |
| | ST-106 Validate Zero-Balance Settlement | Medium | 3 |
| EPIC-3 Trip Visibility & Administration | ST-107 View Ledger, Balances & Settlement | Medium | 3 |

The backlog totals **32 story points**, planned across two one-week sprints.

- **Sprint 1 (26 SP):** ST-101 to ST-105. Goal: capture expenses, normalize currency and calculate settlement. All 26 points were completed.
- **Sprint 2 (6 SP):** ST-106 and ST-107. Goal: validate the settlement and expose the final results. All 6 points were completed.

The report includes the backlog view, the Planning Poker table, the Sprint 1 board in progress and completed, the Sprint 2 board, and the burndown chart. In the reflection I concluded that the estimates were mostly accurate (ST-105 was the biggest item because it holds the optimization logic), that the backlog was ordered by user impact and dependency, and that the burndown showed adequate capacity but some risk of finishing complex work late.

## Lab 3 — Architecture Selection & Component Modelling

**System:** Self-Service Coffee Kiosk System (3 coffee types, 2 sizes, card payment only)
**Chosen architecture:** Layered Architecture

**Justification** (`PES1UG24CS344_Lab3_Justification.pdf`):

- **Requirements map onto layers.** The Presentation layer (touch-screen User Interface), the Business layer (Order Manager, Payment Service, Receipt Printer) and the Data layer (Menu Database) each fit one responsibility, and dependencies flow one way. Microservices would add network overhead a single kiosk does not need, and client-server would create a single point of failure.
- **Easy to maintain and replace parts.** Components talk only through interfaces, so the printer, the payment provider or the menu storage can be swapped without touching the UI.
- **Security:** the Order Manager is the single controlled entry point. It validates every request, the UI never reaches the Payment Service or database directly, and card details stay inside the Payment Service, which talks to the processor over TLS.
- **Performance:** all layers run on one device with in-process calls, menu data is small enough to cache, and receipt printing does not block the UI.
- **Trade-off:** layering adds some indirection and makes independent scaling harder, which is acceptable for a single low-load device.

**Component diagram** (`PES1UG24CS344_Lab3_Component_Diagram.pdf`): a UML component diagram with provided and required interfaces, assembly connectors and numbered data flow. The four interfaces are `IOrderService`, `IPaymentService`, `IReceiptPrinter` and `IMenuData`. The flow for one order is: (1) the customer picks a coffee and the UI sends the order, (2) the Order Manager reads menu and prices from the database, (3) it sends a payment request and receives approved or declined, (4) on approval it sends the details to the Receipt Printer.

---

## Lab 4 — VibeCoding: Dino Run (Python, Pygame)

A single-file side-scrolling endless runner. The starter code had one deliberate bug and three empty feature hooks. I fixed and extended it with ChatGPT, one task at a time, and tested each change myself. The detailed write-up is in `PES1UG24CS344_LAB4/README.md`.

### How to Run

Requires Python 3.10+ and Pygame.

```bash
cd PES1UG24CS344_LAB4
pip install pygame
python game.py
```

**Controls:** `Space`, `Up` or `W` to start, jump and restart after Game Over.

### Tasks Completed

| # | Task | What I did |
|---|------|------------|
| 1 | Fix the high-score bug | The comparison after a collision was backwards, so the high score never updated. It is now `if current > self.high_score:`, followed by saving to `dino_highscore.txt`. |
| 2 | `dino_tint(on_ground)` | Green on the ground, blue while airborne. |
| 3 | `on_obstacle_passed(obstacle, score)` | A consecutive-clear combo counter and a floating `+1  COMBO xN` popup. The combo resets on a crash and on restart. |
| 4 | `max_jumps()` | Returns `2` for a double jump. |

### Testing

I played the game on my Mac and confirmed that the high score updates and persists, the dino changes colour in the air, double jump works and combo popups appear. I also checked the game logic in a script with Pygame stubbed out: a better score replaces the stored best and a worse one does not, `jump_count` stops at 2 and resets on landing, and the combo and popup are created when an obstacle is passed.

### Lab 4 Deliverables

- Gameplay video before changes: `PES1UG24CS344_LAB4/original video.mov`
- Gameplay video after changes: `PES1UG24CS344_LAB4/updated game video.mov`
- Updated code: `PES1UG24CS344_LAB4/game.py`
- AI usage record: `PES1UG24CS344_LAB4/Lab4_AI_Chat_History_.md`

* * *

## Lab 5 — Static Code Analysis: Smart Home Controller (Python)

`smart_home.py` manages smart home devices: it adds devices to rooms, toggles them, sets the thermostat within 16–30, lists devices by room, reports power use and saves state to `home_state.json`. I analysed it with Pylint, Bandit and Flake8, documented 16 issues, and fixed all of them. The detailed write-up is in `PES1UG24CS344_LAB5/README.md`.

### How to Run

```bash
cd PES1UG24CS344_LAB5
python smart_home.py
```

To regenerate the before and after reports: `bash run_analysis.sh`.

### Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.80/10 (26 messages) | **10.00/10** |
| Bandit | 4 issues: 1 High, 1 Medium, 2 Low | No issues, with 2 justified `# nosec` suppressions (B404, B603) |
| Flake8 | 4 issues | 0 issues |

### Key Fixes

1. **Command injection (Bandit B602, High).** `run_scene` ran `subprocess.call("bash scenes/" + name, shell=True)`. It now takes no shell, passes an argument list, and only accepts a bare `*.sh` file that exists in `scenes/`. Names like `x; rm -rf ~` and `../evil.sh` are rejected.
2. **Binding to all interfaces (B104).** The hub address defaults to `127.0.0.1` instead of `0.0.0.0`.
3. **Hard-coded password (B105).** `HUB_PASSWORD` is read from the environment.
4. **Shared mutable default (Pylint W0102, found by running the program).** `settings={}` was shared by every device, so a light showed `{'temperature': 30}` and the fan and TV got a temperature too. Each device now owns its settings, and only the thermostat has `temperature`.
5. **Crash on an unknown device.** `set_temperature` raised `KeyError`. It now prints a message and returns `False`.
6. **Quality and style.** Consistent returns, `encoding="utf-8"`, snake_case names, docstrings, `MIN_TEMP` / `MAX_TEMP` constants, a `main()` guard, and PEP 8 formatting.

The issue table is in `PES1UG24CS344_LAB5/issues.md` and the reflection answers are in `PES1UG24CS344_LAB5/reflection.md`.

### Lab 5 Deliverables

- Cleaned code: `PES1UG24CS344_LAB5/smart_home.py` (original kept as `smart_home_original.py`)
- Issue table: `PES1UG24CS344_LAB5/issues.md`
- Reflection: `PES1UG24CS344_LAB5/reflection.md`
- Reports before and after: `PES1UG24CS344_LAB5/reports/before/` and `reports/after/`

* * *

## Lab 6 — Code & Branch Coverage: Highway Toll (Python)

The assigned repository (`L6_L7_36_highway_toll`) contains `highway_toll.py` with three functions. I wrote two pytest files and measured them with `coverage`: one aimed at line coverage and one at branch coverage.

### Functions Under Test

| Function | Behaviour |
|----------|-----------|
| `toll_for(axles, is_peak, has_fastag)` | Base toll by axle count (2 → 100, 3 → 150, 4 → 250, 5 or more → 400). Fewer than 2 axles raises `ValueError`. Peak hours add 25%. FASTag gives 10% off for 2 axles and 5% off otherwise. The result is rounded to two decimals. |
| `toll_charge(vehicle, axles, is_peak, has_fastag)` | Returns 0 for exempt vehicles (`ambulance`, `fire_engine`), otherwise calls `toll_for`. |
| `pass_advice(trips, axles, pass_price)` | Totals the cost of a list of trips and returns `"buy_pass"`, `"either"` or `"pay_per_trip"` compared with the pass price. |

### How to Run

Requires Python 3.9+ with `coverage` and `pytest`, and the Lab 6 `highway_toll.py` from the assigned repository placed in the same folder.

```bash
cd PES1UG24CS344_LAB6
pip install coverage pytest

# Line (code) coverage
python -m coverage run -m pytest CodeCoverageTest_PES1UG24CS344_highway_toll.py
python -m coverage report -m

# Branch coverage
python -m coverage run --branch -m pytest BranchCoverageTest_PES1UG24CS344_highway_toll.py
python -m coverage report -m
```

### Results

| Test file | Tests | Result |
|-----------|-------|--------|
| `CodeCoverageTest_PES1UG24CS344_highway_toll.py` | 9 | **100% line coverage** (28 of 28 statements) |
| `BranchCoverageTest_PES1UG24CS344_highway_toll.py` | 34 | **100% branch coverage** (18 of 18 branches, 0 partial) |

### Test Design

1. **Code coverage tests.** One small test for each line the two starter tests did not reach: the invalid axle count, the default 400 toll, the peak surcharge, both FASTag discounts, a non-exempt charge, and all three `pass_advice` results.
2. **Branch coverage tests.** Every decision is driven both True and False: `axles < 2`, `axles in BASE_TOLL`, `is_peak`, `has_fastag`, `axles == 2`, `vehicle in EXEMPT`, the trips loop (zero and many iterations), `cost > pass_price` and `cost == pass_price`. It adds boundary and edge cases such as 0 and negative axles, 5 and 9 axles, a case-sensitive exemption (`"Ambulance"` is charged), an empty trip list, and exempt vehicles skipping axle validation.
3. **Line versus branch coverage.** A line can run without every outcome of its `if` being tested. For example, `if is_peak:` has no `else`, so a suite that only uses `is_peak=True` runs every line but never tests skipping the surcharge.

### Lab 6 Deliverables

- Code coverage tests: `PES1UG24CS344_LAB6/CodeCoverageTest_PES1UG24CS344_highway_toll.py`
- Branch coverage tests: `PES1UG24CS344_LAB6/BranchCoverageTest_PES1UG24CS344_highway_toll.py`
- Report with terminal screenshots: `PES1UG24CS344_LAB6/Lab6_Coverage_Report.pdf`

* * *

## Lab 7 — Fuzz Testing with Hypothesis: Highway Toll (Python)

The Lab 7 `highway_toll.py` is a different module from Lab 6. It has three input-parsing functions and a `main()` that reads them from the keyboard. I wrote a Hypothesis test file, used it to find crashes and wrong answers in the original code, then hardened the script so every test passes.

### How to Run

Requires Python 3.9+ (the huge-digit-string test targets Python 3.11+) with `hypothesis` and `pytest`.

```bash
cd PES1UG24CS344_LAB7
pip install hypothesis pytest
python highway_toll.py
python -m pytest test_highway_toll.py
```

### Functions Under Test

| Function | Example input | Output |
|----------|---------------|--------|
| `parse_plate(plate)` | `KA-05-AB-1234` | `('KA', 5, 1234)` |
| `trip_cost(text)` | `3x150` | `450` |
| `axle_class(axles)` | `3` | `truck` (2 car, 3–4 truck, 5 or more heavy) |

### Test Design

`test_highway_toll.py` has **16 tests**. Each function has a no-crash fuzz test on random text and `None`, one on any Python type (numbers, booleans, bytes, lists), and property tests on the expected behaviour.

| Function | Properties tested |
|----------|-------------------|
| `parse_plate` | Never crashes. Valid generated plates round-trip to `(STATE, district, number)`. A wrong number of parts gives `None`. Tricky forms such as Arabic-Indic digits, `+5`, `0_5` and empty parts give `None`. |
| `trip_cost` | Never crashes. Valid `COUNTxRATE` (with `x` or `X`) equals count times rate. Zero or negative trips, more than 1000 trips, and 5000-digit strings give `None`. |
| `axle_class` | Never crashes. Every integer maps correctly and digit strings give the same answer. Floats and booleans give `None`. |

### Bugs Found and Fixed

| Function | What broke it (found by Hypothesis) | Fix |
|----------|--------------------------------------|-----|
| `parse_plate` | `None` raised `AttributeError`. A wrong number of parts and non-numeric parts raised `ValueError`. `int()` silently accepted `' 5'`, `'+5'`, `'0_5'` and non-ASCII digits. | Type check, exactly four parts, ASCII-only letter and digit checks with length limits, and `None` for anything invalid. |
| `trip_cost` | `None` raised `AttributeError`. A missing or extra `x` raised `ValueError`. `-3x150` and `0x150` were accepted. 5000-digit numbers hit Python's int-digit limit. | Type check, exactly one `x`, ASCII digits with length limits, and `1 <= trips <= 1000`, `0 <= rate <= 100000`. |
| `axle_class` | `None` raised `TypeError`, `'abc'` raised `ValueError`, `inf` raised `OverflowError`. `True`, `0`, `1` and negatives were classed as truck, and `2.9` was truncated to `car`. | Accept only an int (not a bool) or a digit string, valid range 2–20, `None` otherwise. |

`main()` now prints a clear "Invalid ..." message instead of crashing and handles end-of-input safely.

### Results

| Code | `pytest test_highway_toll.py` |
|------|-------------------------------|
| Original | 14 failed, 2 passed |
| Fixed | **16 passed** |

Running the fixed program with `KA-05-AB-1234`, `3x150` and `3` prints `('KA', 5, 1234)`, `450` and `truck`. Running it with `KA05AB1234`, `-3x150` and `abc` prints an "Invalid ..." message for each instead of a traceback.

### Lab 7 Deliverables

- Report PDF with screenshots (buggy run, failing tests, fixed run, passing tests): `PES1UG24CS344_LAB7/Lab7_FuzzTesting_Report.pdf`
- Fixed application script: `PES1UG24CS344_LAB7/highway_toll.py`
- Hypothesis test file: `PES1UG24CS344_LAB7/test_highway_toll.py`

* * *

## Notes

- Labs 1 and 2 use the Group Travel Expense Simplification Engine. Lab 3 models a different system, the Self-Service Coffee Kiosk.
- The Lab 6 folder holds the tests and the report but not `highway_toll.py` itself. To re-run those tests, copy the Lab 6 version of the module from the assigned repository next to them. The `highway_toll.py` in the Lab 7 folder is a different file.
