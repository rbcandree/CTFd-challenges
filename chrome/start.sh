#!/bin/bash

cd /opt/app
python3 app.py &

# keeps container running
tail -f /dev/null