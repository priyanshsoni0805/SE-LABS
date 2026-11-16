# Lab 5: Static Code Analysis — Smart Home Device Controller

**Name:** Priyansh Soni  **SRN:** PES1UG24CS344  **File analysed:** `smart_home.py`

`smart_home.py` controls smart home devices. It adds devices to rooms, switches them on and off, sets the thermostat within a safe range (16–30), lists devices by room, reports power use and saves the home state to `home_state.json`. The starter code worked but had security, bug, quality and style problems. I analysed it with Pylint, Bandit and Flake8, documented every finding, and fixed all of them. I also fixed a bug that none of the tools report, which I found by reading the program's output.

## Submission

| Deliverable | File |
|---|---|
| Cleaned code | `smart_home.py` |
| Original starter code (kept for the "before" reports) | `smart_home_original.py` |
| Issue table (16 issues) | `issues.md` |
| Reflection answers | `reflection.md` |
| Reports before the fixes | `reports/before/` |
| Reports after the fixes | `reports/after/` |
| Script that regenerates all six reports | `run_analysis.sh` |

## How to run

```bash
python smart_home.py
```

It runs a short demonstration and needs no input. Output after the fixes:

```
Device not found: Garage Door
Ceiling Light is not a thermostat
Bedroom devices: ['Bedroom Fan', 'Thermostat']
Current power use (W): 1510
Hub address: 127.0.0.1:8080
Light settings: {}
Devices on: ['Ceiling Light', 'Thermostat']
```

It also writes `home_state.json`.

## How the analysis was run

```bash
python -m pip install pylint bandit flake8
python -m pylint smart_home.py > pylint_report.txt
python -m bandit -r smart_home.py > bandit_report.txt
python -m flake8 smart_home.py > flake8_report.txt
```

`bash run_analysis.sh` does this for both the original and the fixed file and saves the reports under `reports/before/` and `reports/after/`.

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.80 / 10 (26 messages) | **10.00 / 10** |
| Bandit | 4 issues: 1 High, 1 Medium, 2 Low (B602, B104, B105, B404) | No issues identified, with 2 `# nosec` suppressions (see below) |
| Flake8 | 4 issues (E203, E302, E261, E501) | 0 issues (empty report) |

### About the two suppressions
After removing `shell=True`, Bandit still reports two informational findings: B404 (`import subprocess`) and B603 (a subprocess call without a shell). Both are marked `# nosec`, because the call uses an argument list and validated input. They are suppressed on purpose, not fixed, so the Bandit report reads "No issues identified" while the suppressed count shows 2.

## Main issues found

Line numbers refer to `smart_home_original.py`. The full table of 16 issues is in `issues.md`.

| Issue | Tool / code | Severity | Fix |
|-------|-------------|----------|-----|
| `subprocess.call("bash scenes/" + name, shell=True)` allows command injection and path traversal | Bandit B602 | **High** | No shell. Arguments are a list, and the name must be a bare `*.sh` file inside `scenes/` that exists. |
| Hub bound to `0.0.0.0` (all interfaces) | Bandit B104 | Medium | Default to loopback `127.0.0.1`. |
| Hard-coded `HUB_PASSWORD` | Bandit B105 | Low | Read from the `HUB_PASSWORD` environment variable. |
| Mutable default argument `settings={}` shared by every device | Pylint W0102 | **Bug** | `settings=None`, and each device gets its own copy. |
| `set_temperature` crashes with `KeyError` on an unknown device | none (found by reading) | Bug | Use `DEVICES.get(...)`, print a message and return `False`. |
| Inconsistent returns in `toggle_device` | Pylint R1710 | Quality | Explicit `return None`. |
| `open()` without an encoding | Pylint W1514 | Quality | `encoding="utf-8"`. |
| camelCase names, missing docstrings, magic numbers 16 / 30, `main()` runs on import | Pylint C0103, C0114, C0116 | Style / design | snake_case, docstrings, `MIN_TEMP` / `MAX_TEMP`, `if __name__ == "__main__":`. |
| Spacing, blank lines, comment spacing, 80-character line | Flake8 E203, E302, E261, E501 | Style | Reformatted. |

### The bug the tools did not explain
Running the original program printed `Light settings: {'temperature': 30}`. A light should not have a temperature. The shared `{}` default meant every device pointed at one dictionary, so setting the thermostat added a `temperature` to the light, fan and TV, and all of them were saved to the JSON file. Pylint flags the pattern (W0102) but only running the program shows its effect. After the fix, only the thermostat has a temperature.

## Behaviour changes

The demo output is the same except for the hub address and the light settings, which are now correct. These changes also affect other callers:

- **Function and argument names are now snake_case** (`addDevice` became `add_device`, `deviceName` became `device_name`, and so on), and the registry `devices` is now `DEVICES`. Old callers must be updated.
- **`run_scene` raises `ValueError`** for any name that is not a plain `*.sh` file in `scenes/`.
- **`set_temperature` returns `False`** for an unknown device instead of raising.
- **The hub defaults to `127.0.0.1`**, so it is no longer reachable from other machines unless changed on purpose.

## Testing

I ran the original and the fixed program and compared their output and the saved JSON. I also called `run_scene` with unsafe and invalid names.

| Check | Result |
|---|---|
| Original run, light, fan and TV settings | Each contains `temperature: 30` (the shared-dictionary bug) |
| Fixed run, light, fan and TV settings | `{}`; only the thermostat has `temperature: 30` |
| `set_temperature("Thermostat", 35)` | Clamped to 30 |
| `run_scene("x; rm -rf ~")` | Rejected with `ValueError` |
| `run_scene("../evil.sh")` | Rejected |
| `run_scene("nofile.sh")` | Rejected (file does not exist) |
| `run_scene("a.txt")` | Rejected (not `.sh`) |

## Limitations

- `HUB_PASSWORD` is read from the environment but not used anywhere yet, and defaults to an empty string if the variable is not set.
- There is no `scenes/` folder in the repo, so `run_scene` can only reject input right now. A valid scene script has not been run through it.
- Device state is held in a module-level dictionary, which is simple but harder to test than passing state in.
- No automated unit tests were written. Checks were done by running the program and the three tools.
- `README_SUBMISSION.md` mentions three commits (Bandit, Pylint, Flake8) but a git history is not part of the files here, so I could not check them.
