#!/bin/bash

yt-dlp --cookies-from-browser firefox --retries infinite -S "height:720" -o tmp_vid $1
pipenv run python frame_munger.py tmp_vid.* && rm tmp_vid.*

