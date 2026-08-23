# Unit Converter

Standalone local engineering unit conversion service backed by Pint. It provides family-based conversion, dimensional expressions, and a small browser UI at `http://127.0.0.1:5065`.

## Deployment modes

Unit Converter is independently deployable as a complete web app. It can be developed, tested, and
run without `ml_server` or any other platform tool; the portal optionally links to its stable
service URL for a common intranet experience.

## Production release 0.2.0

The browser UI is fully wired to the API and includes a scientific help page at
`/help`. The stable API is rooted at `/api/v1/units`; the earlier `/api/*`
routes remain as compatibility aliases. Absolute and interval temperatures are
explicitly different modes.

Install and run with the production WSGI server:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
unit-converter
```

The service listens on `127.0.0.1:5065`. Put an intranet reverse proxy with TLS
in front when it is exposed beyond the local host. Verify `/api/health` before
switching traffic. Roll back by reinstalling the previously pinned wheel or Git
tag and restarting the service.

## Release notes

- Added the documented `/api/v1/units/*` contract while preserving legacy APIs.
- Added correct absolute-versus-interval temperature conversion.
- Connected all browser controls to the service and added accessible results.
- Added scientific help, an SVG algorithm flow, production security headers,
  request limits, and a Waitress entry point.
