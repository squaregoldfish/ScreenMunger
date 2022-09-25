#!/bin/bash

MAX_CHANGED_PIXELS=103680

# Get the requested minute
NUM_CHECK='^[0-9]+$'
minute=$1

if nc -z yaffle 22 -w 2
then
  exit
fi

if ! [[ $minute =~ $NUM_CHECK ]]
then
  minute=0
fi

if [[ $minute -lt 0 ]]
then
  minute=0
fi

if [[ $minute -gt 59 ]]
then
  minute=59
fi

# Zero pad
minute=$(printf "%02d" $minute)

# Get the last image we processed
last_sorted=""

if [[ -e "last_sorted.dat" ]]
then
    last_sorted=$(cat last_sorted.dat)
fi

# Get the latest image for the specified minute
# We won't cross the day threshold
last_shot_dir="uploads/$(date '+%Y%m%d')"
last_shot=$(find "${last_shot_dir}"/*"${minute}"00.png|sort|tail -1)

# If there's an image
if [ -n "$last_shot" ]
then
  # See if we're doing a new image
  if [[ "$last_shot" != "$last_sorted" ]]
  then
    # Make sure the image has changed enough to justify
    # a new process
    process=1

    if [ -n "$last_sorted" ]
    then
      changed_pixels=0

      if [ -f "$last_sorted" ]
      then
        changed_pixels=$(compare -metric AE "$last_sorted" "$last_shot" null: 2>&1)
      fi

      if [ "$changed_pixels" -lt "$MAX_CHANGED_PIXELS" ]
      then
        process=0
      fi
    fi

    if [[ $process == 1 ]]
    then
      filename=$(basename "$last_shot")
      pipenv run python sort_image.py "$last_shot" "A screenshot with pixels sorted by random criteria" "${filename:0:4}-${filename:4:2}-${filename:6:2} ${filename:8:2}:${filename:10:2}:${filename:12:2}"

      # Log the sorted file
      echo "$last_shot" > last_sorted.dat
    else
      vidfile=`ls -t uploads/video |tail -1`
      if [ -n "$vidfile" ]
      then
        pipenv run python postimage.py "uploads/video/$vidfile" "Random frame from a video sorted by random criteria"
        rm "uploads/video/$vidfile"
      fi
    fi
  fi
fi

#Sequence of stripes showing the average pixel colour of a frame of a video every 0.1 seconds
