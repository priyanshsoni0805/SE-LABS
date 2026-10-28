# Lab 5 – Issue Table: `smart_home.py`

**Name:** Priyansh Soni  **SRN:** PES1UG24CS344

Line numbers refer to the **original** file (`smart_home_original.py`).
Severity: Bandit severity/confidence where applicable. Items marked ★ were not
only style problems but real bugs / vulnerabilities.

## A. Bandit (security)

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 ★ | `subprocess.call(..., shell=True)` with string concatenation (B602) | Security – **HIGH** | 51 | `runScene` builds a shell command from the caller's `sceneScript`. Input such as `x; rm -rf ~` or `../../evil.sh` runs arbitrary commands (command injection / path traversal). | Removed `shell=True`; pass an argument list to `subprocess.run(["/bin/bash", script], check=True)`. Validate that the name is a bare `*.sh` file that exists in `scenes/` (rejects `;`, `..`, `/`). |
| 2 ★ | Binding to all interfaces `"0.0.0.0"` (B104) | Security – **MEDIUM** | 4 | Hub address exposes the service on every network interface, including untrusted networks. | Default to loopback `127.0.0.1`. |
| 3 ★ | Hard-coded password (B105) | Security – LOW | 7 | `HUB_PASSWORD = "smarthome-demo"` is committed to source control and visible to anyone with the repo. | Read from environment: `os.environ.get("HUB_PASSWORD", "")`. |
| 4 | `import subprocess` (B404) | Security – LOW | 2 | Informational: subprocess is a risky module. | Usage is now safe (list args, validated input) so the import is annotated `# nosec B404`. The call itself carries `# nosec B603` (B603 = "subprocess without shell, check input"), justified by the validation above. |

## B. Pylint (quality / bugs)

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 5 ★ | Mutable default argument `settings={}` (W0102 dangerous-default-value) | Bug | 11-13 | One dict is shared by **every** device. Running the program shows `Light settings: {'temperature': 30}` and the light, fan and TV all get a `temperature` saved to JSON – setting the thermostat changes all of them. | `settings=None`, then `dict(settings) if settings else {}` so each device owns its settings. Output now: light/fan/TV `{}`, only thermostat has `temperature`. |
| 6 ★ | Crash on unknown device in `setTemperature` | Bug (logic) | 24 | `devices[deviceName]` raises `KeyError` for a name that doesn't exist (while `toggleDevice` handles it gracefully). | Use `DEVICES.get(name)`; print message and return `False`. |
| 7 | Inconsistent return statements (R1710) | Quality | 16-20 | `toggleDevice` returns a bool in one path and implicitly `None` in the other. | Added explicit `return None`. |
| 8 | `open()` without `encoding` (W1514 unspecified-encoding) | Quality / portability | 41 | Encoding depends on the OS locale. | `open(file_name, "w", encoding="utf-8")`. |
| 9 | Missing module and function docstrings (C0114, C0116) | Style | 1, 11, 16, 23, 32, 36, 40, 45, 49, 54 | No documentation anywhere. | Added a module docstring and one for every function. |
| 10 | Naming not snake_case (C0103 invalid-name) | Style | 11-67 | `addDevice`, `deviceName`, `fileName`, `sceneScript`, global `devices`… | Renamed to `add_device`, `device_name`, `file_name`, `scene_script`; module-level mutable registry → `DEVICES`. |
| 11 | Magic numbers 16 / 30 | Quality | 28 | Safe temperature range hidden inside an expression. | Named constants `MIN_TEMP`, `MAX_TEMP`. |
| 12 | `main()` runs on import | Design | 72 | Importing the module executes the demo. | `if __name__ == "__main__": main()`. |

## C. Flake8 (formatting – PEP 8)

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 13 | E203 whitespace before `:` | Style | 6 | `"light" : 10` | `"light": 10`. |
| 14 | E302 expected 2 blank lines, found 1 | Style | 40 | Only one blank line before `def saveState`. | Added second blank line. |
| 15 | E261 at least two spaces before inline comment | Style | 66 | `hubAddress()) # for app setup` | Two spaces before `#`. |
| 16 | E501 line too long (80 > 79) | Style | 68 | The "Devices on" `print` line is 80 characters. | Extracted `devices_on` list into a variable. |

## Results (from running the tools: `bash run_analysis.sh`)

| Tool | Before | After |
|------|--------|-------|
| Bandit | 1 High, 1 Medium, 2 Low (B602, B104, B105, B404) | 0 reported (B404 and B603 suppressed with `# nosec` and a written justification) |
| Pylint | 4.80 / 10 | 10.00 / 10 |
| Flake8 | 4 issues (E203, E302, E261, E501) | 0 issues |

Reports: `reports/before/` (original `smart_home_original.py`) and
`reports/after/` (fixed `smart_home.py`).

## D. Bug the tools do NOT flag (found by running the program)

The README hints that "not every problem is something a tool will flag". Running
the original program printed `Light settings: {'temperature': 30}`: a *light*
had a thermostat setting. This is issue #5 – Pylint flags the pattern
(W0102) but only running the program reveals its effect.
