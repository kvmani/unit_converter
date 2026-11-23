# Unit Converter — specification

The contract that code, tests and help must satisfy. A change to anything here is a deliberate,
versioned change recorded in `CHANGELOG.md`.

## Purpose and boundaries

- Privacy-first, air-gapped engineering unit conversion backed by Pint, with a small browser UI.
- Standalone: runs without `ml_server` or any other tool; the portal only links to its URL.
- Listens on `127.0.0.1:5065` (Waitress, `unit-converter` entry point); `/api/health` reports
  liveness and is used by the suite installer.

## API (stable base `/api/v1/units`)

| Method and path | Request | 200 response |
| --- | --- | --- |
| `GET /api/v1/units/families` | — | `{"families": [...]}` |
| `GET /api/v1/units/units?family=<name>` | family, case-insensitive | `{"units": [{"symbol", "aliases", "dimension"}]}`; unknown family → 404 `BAD_INPUT` |
| `POST /api/v1/units/convert` | JSON `value`, `from`, `to`, optional `mode` = `absolute` (default) or `interval` | `{"ok": true, "result", "unit", "text", ...}` |
| `POST /api/v1/units/convert/expression` | JSON `expression`, e.g. `"200 MPa * 10 mm^2 to N·mm"` | `{"ok": true, "result", "unit", ...}` |

**Legacy aliases (must keep working):** `GET /api/families`, `GET /api/units/<family>`,
`POST /api/convert` (fields `from_unit`/`to_unit`), `POST /api/expressions`.

**Errors:** 4xx with `{"ok": false, "error_code": "INVALID_UNIT|DIMENSION_MISMATCH|LIMIT_EXCEEDED|BAD_INPUT", "message": "..."}`.

**Planned, not implemented:** `POST /api/v1/units/batch/convert` (multipart `file` + `options`
JSON, returns a CSV/XLSX attachment; headers carry `[unit]`). Treat it as a spec for future work.

## Unit semantics

- Pint registry with aliases: Å = angstrom = 1e-10 m; micron = micrometer = µm;
  ksi = kilopound-force per square inch; μΩ·cm; MPa; GPa.
- Temperature: `mode="absolute"` uses offset conversion (25 °C ↔ 298.15 K);
  `mode="interval"` maps differences exactly (Δ25 °C ↔ 25 K), never by offset formulas.
- Expression grammar: `<scalar> <unit> [op <scalar> <unit>]* "to" <unit>`, ops `*` and `/`,
  evaluated with Pint quantities; reject invalid dimensions with `DIMENSION_MISMATCH`.

## Limits and security

- Request bodies are limited to 1 MiB (413 when exceeded); wrong MIME → 415.
- Every response sets `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, a
  restrictive `Permissions-Policy` and a `default-src 'self'` Content-Security-Policy; API
  responses are `Cache-Control: no-store`.
- No persistent logging of user input; no cookies, localStorage or IndexedDB; no network traffic
  beyond localhost (assets such as MathJax are vendored).

## Test matrix (minimum coverage)

- Engine: MPa ↔ N/mm² (1:1); MPa ↔ ksi (≈145.038 psi per MPa); Å ↔ nm ↔ m; kJ/mol ↔ eV
  (Pint's N_A and e); μΩ·cm ↔ Ω·m (1 μΩ·cm = 1e-8 Ω·m); W/(m·K) round trips; Pa·s ↔ cP
  (1 cP = 1e-3 Pa·s); m²/s identity; absolute and interval temperature cases; dimension mismatch
  raises a clean error.
- API: JSON validation, 415 for wrong MIME, 413 over limits, legacy aliases, security headers.
- UI and help: page loads with no external requests; help equations render offline.
