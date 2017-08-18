#!/usr/bin/env bash
#gunicorn --bind 0.0.0.0 --workers 128 app:api >/dev/null
gunicorn --bind 0.0.0.0:8002 --workers 4 app:api >/dev/null
