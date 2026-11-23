# AGENTS.md — Unit Converter

Privacy-first, air-gapped engineering unit converter: a Pint-backed Flask service with a browser
UI and scientific help page, served by Waitress on `127.0.0.1:5065`. It runs on its own; the
`ml_server` portal links to it and `ml_server_deploy` ships it. This file is the operating contract
for every coding agent (Codex, Claude, Gemini, …) and human contributor; it is the only
agent-instruction file in the repository.

**Order of authority:** the owner's instruction for the task → this file →
[docs/SPECIFICATION.md](docs/SPECIFICATION.md) → [README.md](README.md) → code comments.

## Cardinal rules (owner-mandated, every repository)

1. **Fetch before you change anything.** Start every task with
   `git fetch origin && git pull --rebase --autostash origin main`. Several people and agents push
   to this repository; never build on a stale checkout.
2. **Work on `main` only.** Commit and push directly to `main` unless the owner names another
   branch for the task. No feature branches or pull requests by default. Fetch again before
   pushing; if the push is rejected, `git pull --rebase origin main`, rerun the affected tests,
   then push. Never force-push or rewrite published history.
3. **Keep the progress ledger current:** [`docs/PROGRESS.md`](docs/PROGRESS.md). Before coding, add (or claim)
   the task entry: goal, plan, who is working on it, date. After each meaningful step record what
   was done, the commit, test evidence, decisions, blockers and the next step. Commit the ledger
   with the work it describes. A new session must be able to resume from the ledger and git
   history alone, without the chat that started the work.
4. **Targeted tests for ordinary changes.** Run only the tests that cover what you touched (see
   [Tests](#tests)). Run the full suite only when preparing a release or when the owner asks.
5. **CI runs only on request.** GitHub Actions workflows start by `workflow_dispatch` only;
   tag-triggered release workflows are the single exception. Never add push, pull-request or
   schedule triggers, and never start a workflow unless the owner asks.
6. **Be honest.** Never report a check as passed unless you ran it and saw it pass; record skipped
   checks and the reason. Never weaken, skip or delete a test to make it pass.
7. **Keep git clean.** Commit sources and canonical assets only: no secrets, real personal data,
   virtual environments, caches, logs or build output.

The cardinal rules decide *how work is done* (sync, branch, ledger, test scope, CI). The project
rules in this file decide *what this repository must achieve and protect*; nothing generic here
relaxes them. If a project rule and a cardinal rule genuinely conflict, stop and ask the owner.

## Project rules

- **The specification is the contract.** API routes, error codes, unit semantics, limits and the
  minimum test matrix are in [docs/SPECIFICATION.md](docs/SPECIFICATION.md). Change it only
  deliberately, together with code, tests, help and CHANGELOG.
- **Keep the legacy `/api/*` aliases and `/api/health` working**; the portal and suite rely on them.
- **Absolute and interval temperatures are different modes.** Never convert a temperature
  difference with an offset formula.
- **Privacy and air gap:** no network traffic beyond localhost, no persistent logging of input, no
  cookies or browser storage; vendored assets only.
- **Plugin conventions:** for portal integration follow `kvmani/ml_server` (API expectations) and
  `kvmani/pdf_tools` (code organisation) — read them only when the task touches integration.
- Commit subjects use conventional prefixes (`feat:`, `fix:`, `docs:`, `test:`); keep diffs small.
- **Release bookkeeping:** `VERSION` in `app.py`, `pyproject.toml`, README release notes and
  `CHANGELOG.md` move together.

## Quality bar

- The smallest change that fully solves the task, following existing patterns; no dead code.
- Reject bad input with the documented `error_code` and a clear message; never return a silently
  wrong value.
- Type hints and docstrings on public functions (purpose, parameters with units, returns, errors).
- Every behaviour change ships with a test from the spec's matrix, including the failure case.
- User-visible changes update `templates/help.html`, README and CHANGELOG in the same commit.

## How to work

1. Sync (cardinal rule 1) and read the ledger.
2. Read the relevant section of the specification, the code you will change and its tests.
3. Plan files, tests and docs; note them in the ledger. Implement in small verified steps,
   committing, pushing and updating the ledger after each.

## Tests

```bash
pip install -r requirements.txt -r requirements-test.txt
python -m pytest tests/test_app.py -q -k <keyword>   # targeted (ordinary changes)
python -m pytest                                      # full suite (release or on request)
```

| You changed | Run |
| --- | --- |
| conversion, expressions, routes, headers in `app.py` | `tests/test_app.py` (narrow with `-k`) |
| `templates/help.html`, MathJax config | `tests/test_help_mathematics.py` |
| UI (`static/app.js`, `templates/index.html`) | `tests/test_app.py -k ui` if present, plus a manual check in the browser |

## Run

```bash
python -m pip install -e .
unit-converter          # http://127.0.0.1:5065 ; verify /api/health
```

## Definition of done

- [ ] Behaviour matches the specification; targeted tests pass and were run.
- [ ] Help page, README and CHANGELOG updated where behaviour is user-visible.
- [ ] Legacy routes and `/api/health` still respond; no external requests introduced.
- [ ] Ledger updated; committed and pushed to `main`.

## Map

| Need | Read |
| --- | --- |
| API, error codes, unit semantics, limits, test matrix | [docs/SPECIFICATION.md](docs/SPECIFICATION.md) |
| Install, deployment modes, release notes | [README.md](README.md) |
| Version history | [CHANGELOG.md](CHANGELOG.md) |
| Original scaffold plan (historical only) | [docs/history/original_codegen_playbook.md](docs/history/original_codegen_playbook.md) |
| Current work and history | [docs/PROGRESS.md](docs/PROGRESS.md) |
