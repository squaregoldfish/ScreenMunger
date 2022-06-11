#!/bin/bash

TMPDIR='/tmp'

metadata=`yt-dlp -j $1`

title=`echo $metadata | sed 's/.*"title": "\(.*\)", "formats".*/\1/g'`
filename="${TMPDIR}/${title}.mp4"

if `echo $metadata | grep -q "22 - "`
then
  yt-dlp -f "best[height=720]" --recode-video mp4 -o "$filename" $1
else
  yt-dlp --recode-video mp4 -o "$filename" $1
fi

pipenv run python frame_munger.py "$filename" && rm "$filename"