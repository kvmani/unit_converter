# AGENTS.md — Execution Playbook for Codegen Agent
## For API requirement or how to be able to plug into ml_server website as a plugin refer to repo: https://github.com/kvmani/ml_server
## Also refer to repo:https://github.com/kvmani/pdf_tools for code organization and expections for being able to be pluged into the ml_server website as a plugin.
## Objective
Implement a **privacy‑first**, **air‑gapped** Unit Converter repo `units_converter` with:
- Core conversion engine (`Converter`)
- Flask API (`/api/v1/units/*`)
- Temporary 3‑panel UX (static) for testing
- Comprehensive tests

## Repository Tasks (Checklist)
- [ ] Scaffold `pyproject.toml`, `units_converter/`, `tests/`, `static/`, `scripts/`.
- [ ] Engine: Pint registry + aliases + expression parsing + interval temperature logic.
- [ ] API: Flask blueprint with routes, JSON validation, error handling, limits.
- [ ] Static UX: 3‑panel HTML/CSS/JS; keyboard navigation; copy buttons; swap units.
- [ ] Tests: pytest + hypothesis; API schema tests; 
- [ ] Docs: README with usage & ml_server integration; this AGENTS.md.
- [ ] License: MIT.

## Directory Layout (Target)
```
units_converter/
  units_converter/
    __init__.py
    config.py
    engine/
      __init__.py
      converter.py
      registry_data.py
    api/
      __init__.py
      app.py            # create_app()
      routes.py         # Blueprint
      schemas.py
      errors.py
    batch/
      __init__.py
      parser.py
      exporter.py
    ui_dev/
      index.html
      styles.css
      app.js
  tests/
    test_engine_basic.py
    test_engine_temperature.py
    test_engine_compound.py
    test_api_convert.py
    test_api_expression.py
    test_api_batch_csv.py
    test_ui_smoke.py
  scripts/
    dev_server.sh
  pyproject.toml
  README.md
  AGENTS.md
  LICENSE
```

## API Contract (Authoritative)
**Base**: `/api/v1/units`

- `GET /families` → 200 `{ "families": [...] }`
- `GET /units?family=pressure` → 200 `{ "units": [{ "symbol":"MPa","aliases":["N/mm^2"],"dimension":"pressure" }, ...] }`
- `POST /convert` → 200 `{ "ok": true, "result": <float>, "unit": "<symbol>", "text": "<pretty>" }`
  - Body: `value: number|string`, `from: string`, `to: string`, `mode: "absolute"|"interval"`, optional `sig_figs`, `decimals`, `notation`.
- `POST /convert/expression` → 200 `{ "ok": true, "result": <float>, "unit": "<symbol>" }`
  - Body: `expression: string` (e.g., `"200 MPa * 10 mm^2 to N·mm"`)
- `POST /batch/convert` (multipart form)
  - Fields: `file`, `options` (JSON). Returns CSV/XLSX stream with `Content-Disposition: attachment`.

**Errors**: 4xx with `{ "ok": false, "error_code": "INVALID_UNIT|DIMENSION_MISMATCH|LIMIT_EXCEEDED|BAD_INPUT", "message": "..." }`

## Limits & Security

- Disable MIME sniffing; set `X-Content-Type-Options: nosniff`.
- No persistent logging; no cookies/localStorage/IndexedDB.

## Unit Semantics
- Use Pint with custom registry:
  - Aliases: Å=angstrom=1e-10 m; micron=micrometer=µm; ksi=kilopound_force_per_square_inch; μΩ·cm; MPa; GPa.
  - Temperature: `mode="interval"` maps Δ°C <-> K exactly, not offset formulas.
- Expression grammar: `<scalar> <unit> [op <scalar> <unit>]* "to" <unit>`; ops: `*`, `/`. Perform with Pint Quantity operations; reject invalid dimensions.

## Testing Matrix
- Engine:
  - MPa↔N/mm² (1 MPa == 1 N/mm²)
  - MPa↔ksi (~145.038 psi/MPa)
  - Å↔nm↔m
  - kJ/mol ↔ eV (use NA and e charge constants built into Pint)
  - μΩ·cm ↔ Ω·m (1 μΩ·cm = 1e-8 Ω·m)
  - W/m·K round‑trips
  - Pa·s ↔ cP (1 cP = 1e-3 Pa·s)
  - m²/s (diffusivity) identity
  - Temperature: 25°C ↔ 298.15 K absolute; Δ25°C ↔ 25 K interval
  - Dimension mismatch raises clean error
- API:
  - JSON schema validation
  - 415 for wrong MIME, 413 for over limits
  - Batch CSV round‑trip (headers with `[unit]`)
- UI smoke:
  - Load index.html; no external requests; basic interactions callable.

## Done Definition
- `scripts/dev_server.sh` runs Flask on `http://127.0.0.1:5007/` and serves `/ui_dev/index.html`.
- `pytest -q` passes locally.
- README shows examples and curl snippets.
- No network traffic outside localhost (grep sources).

## Commit Style
- Conventional commits (`feat:`, `fix:`, `docs:`, `test:`).
- Small, reviewable diffs.
