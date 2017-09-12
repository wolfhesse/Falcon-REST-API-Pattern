#!/usr/bin/env bash

### server_name rcs2_wc.webhooks.devsys.base.wolfspool.at
###                webhook8002.s1.base.wolfspool.at;


cd app
#gunicorn --bind 0.0.0.0 --workers 128 app:api >/dev/null
gunicorn --bind 0.0.0.0:8002 --workers 4 app:api >/dev/null
