#!/bin/bash

yt-dlp --cookies-from-browser firefox --retries infinite -S "height:720" -o tmp_vid $1
source venv/bin/activate
pipenv run python frame_munger.py tmp_vid.* && rm tmp_vid.*

