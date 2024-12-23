#!/bin/bash

vidfile=`ls -t uploads/video |tail -1`
if [ -n "$vidfile" ]
then
    pipenv run python postimage.py "uploads/video/$vidfile" "Random frame from a video sorted by random criteria, or stripes coloured by each frame of a video"
    rm "uploads/video/$vidfile"
fi

