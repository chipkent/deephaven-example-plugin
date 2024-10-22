#!/bin/bash

rm -rf ./venv
python3.12 -m venv ./venv-server
source ./venv-server/bin/activate
python -m pip install --upgrade pip
python -m pip install deephaven_server
python -m pip install ./server
# deephaven server --jvm-args "-Xmx4g -Dauthentication.psk=YOUR_PASSWORD_HERE"
python server.py