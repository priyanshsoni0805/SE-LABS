# Lab 5 – Reflection

**Name:** Priyansh Soni  **SRN:** PES1UG24CS344

> The handout PDF did not print the reflection questions, so these are the four
> standard Lab 5 questions.

**1. Which issues were the easiest and which the hardest to fix?**
Easiest: Flake8 formatting (E203, E302, E261, E501) and Pylint docstring/naming
messages – mechanical and with no behavioural risk. Hardest: the
`subprocess ... shell=True` finding (B602). Simply deleting `shell=True` isn't
enough; I had to decide what input is legitimate and validate it (bare `*.sh`
file inside `scenes/`), then test that `x; rm -rf ~` and `../evil.sh` are rejected.
The mutable default argument was easy to fix but the hardest to *notice* in
practice, because its effect (all devices sharing one `settings` dict) only shows
in the program's output.

**2. Did the tools report false positives, or anything you'd choose not to fix?**
After fixing `run_scene`, Bandit still reports B404 (import subprocess) and
B603 (subprocess call without shell). These are informational: the call uses a
list of arguments and validated input, so I suppressed them with `# nosec` and a
comment explaining why. A `nosec` should always carry a reason, otherwise it just
hides problems. The unused `HUB_PASSWORD` constant is a gentle reminder that
code and config are incomplete – the tools can't tell me whether it should be used.

**3. How would you integrate static analysis into a real workflow?**
Run Flake8, Pylint and Bandit as a pre-commit hook locally and again as a CI job
on every pull request, failing the build on Bandit High/Medium findings, any
Flake8 error, and a Pylint score below an agreed threshold (e.g. 9.5). Keep the
config (`.pylintrc`, `setup.cfg`/`.flake8`, `bandit.yaml`) in the repo so everyone
gets the same rules, and review every `# nosec` / `# pylint: disable` in code review.

**4. What tangible improvements did you see in code quality, readability and security?**
- *Security:* no command injection or path traversal in `run_scene`; no secret in
  source control; hub no longer listens on every interface by default.
- *Correctness:* each device now has its own settings (light/fan/TV no longer get a
  `temperature`), unknown devices no longer crash `set_temperature`, and
  `toggle_device` has a consistent return.
- *Readability/maintainability:* snake_case names, docstrings, named constants,
  a `main()` guard so the module can be imported and tested, and PEP 8
  formatting. Static analysis caught the security problems and most of the
  quality problems, but the shared-settings bug only became obvious from running
  the program, so tools complement – not replace – testing and code review.
