#!/bin/bash
source venv/bin/activate
pipenv --bare run python -W ignore frame_munger.py "$@"
