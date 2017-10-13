#!/usr/bin/env bash

### server_name
###
###	formerly: rcs2_wc.webhooks.devsys.base.wolfspool.at
###     formerly: webhook8002.s1.base.wolfspool.at;
###
### webhooks.base.wolfspool.at


cd app
gunicorn --bind 0.0.0.0:8002 --workers 4 app:api >/dev/null
