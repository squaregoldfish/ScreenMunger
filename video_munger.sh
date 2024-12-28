#!/bin/bash
source venv/bin/activate
pipenv run python video_munger.py "$1"
