#!/bin/bash

rm -rf ./venv
python3.12 -m venv ./venv-client
source ./venv-client/bin/activate
python -m pip install --upgrade pip
python -m pip install ./client
python client.py
