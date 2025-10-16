#!/usr/bin/env bash
set -euo pipefail

export FLASK_APP=units_converter.api.app:create_app
export FLASK_RUN_PORT=5007
export FLASK_RUN_HOST=127.0.0.1

python -m flask run
