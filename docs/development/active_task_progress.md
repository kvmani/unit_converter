# Progress ledger

The resume point for all work in this repository (AGENTS.md, cardinal rule 3). Claim a task in
**Active** before coding, checkpoint in **Task log** after each meaningful step, and move the row
to **Done** with its commit when finished. Newest entries first; keep them short and factual.

## Active

| Task | Who | Started | Status | Next step |
| --- | --- | --- | --- | --- |

## Task log

<!-- Copy this block for each task:
### YYYY-MM-DD — <task>
- Goal:
- Plan (files, tests, docs):
- Done (commits):
- Tests run (command → result):
- Decisions / assumptions:
- Blockers / open questions:
- Next step:
-->

### 2026-11-23 — Agent instructions refactor (done)
- Goal: replace the one-time scaffold playbook with an operating AGENTS.md for every agent
  (Codex, Claude, Gemini): cardinal rules, quality bar, test table, map.
- Rule migration: the API contract, error codes, limits and security, unit semantics and testing
  matrix moved to `docs/SPECIFICATION.md`, updated to the implemented service (port 5065, legacy
  aliases, security headers); the unimplemented batch endpoint is marked "planned". The
  ml_server/pdf_tools references and commit style stay in AGENTS.md. The full original playbook is
  archived verbatim in `docs/history/original_codegen_playbook.md`.
- Removed two committed release logs from `logs/` and ignored `logs/` and `*.log`.
- Added this ledger and `.gemini/settings.json`.
- Tests run: none needed (documentation and repository hygiene only).

## Done

| Date | Task | Commit |
| --- | --- | --- |
| 2026-11-23 | Agent instructions refactor; removed committed logs | see git log |
