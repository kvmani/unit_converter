# Units Converter

An air-gapped, privacy-first unit conversion engine with a Flask API and temporary testing UX.

## Features

- Pint-powered conversion engine with aliases tailored for engineering and materials science.
- Flask API under `/api/v1/units` for single and expression conversions plus batch CSV processing.
- Offline HTML/CSS/JS three-panel UX for manual testing, with in-memory history and favorites.
- Strict JSON error contracts and security headers.
- Pytest + Hypothesis coverage across engine, API, batch, and UX smoke scenarios.

## Getting Started

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -e .[test]
```

### Development Server

Serve the API and static UX locally:

```bash
./scripts/dev_server.sh
```

Then open `http://127.0.0.1:5007/` in a browser. All assets are hosted locally.

### Running Tests

```bash
pytest -q
```

## API Examples

```bash
curl -s http://127.0.0.1:5007/api/v1/units/families

curl -s "http://127.0.0.1:5007/api/v1/units/units?family=pressure"

curl -s -X POST http://127.0.0.1:5007/api/v1/units/convert \
  -H "Content-Type: application/json" \
  -d '{"value":200,"from":"MPa","to":"ksi","mode":"absolute","sig_figs":4}'
```

## Batch CSV Usage

Upload a CSV with headers including units (e.g. `stress[MPa]`). Provide JSON options indicating the target units.

```bash
curl -s -X POST http://127.0.0.1:5007/api/v1/units/batch/convert \
  -F "file=@data.csv" \
  -F 'options={"targets":{"stress":"ksi"}}' \
  -o converted.csv
```

## Project Structure

See `AGENTS.md` for the full expected layout and acceptance criteria.
