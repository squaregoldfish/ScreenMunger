#!/bin/bash

MAX_CHANGED_PIXELS=103680

# Get the requested minute
NUMCHECK='^[0-9]+$'
minute=$1

if ! [[ $minute =~ $NUMCHECK ]]
then
   minute=0
fi

if [[ $minute < 0 ]]
then
  minute=0
fi

if [[ $minute > 59 ]]
then
  minute=59
fi

# Zero pad
minute=`printf "%02d" $minute`

# Get the last image we processed
lastsorted=""

if [[ -e "lastsorted.dat" ]]
then
    lastsorted=`cat lastsorted.dat`
fi

# Get the latest image for the specified minute
# We won't cross the day threshold
lastshotdir="uploads/`date '+%Y%m%d'`"
lastshot=`ls -tr ${lastshotdir}/*${minute}00.png|tail -1`

# If there's an image
if [ -n "$lastshot" ]
then
  # See if we're doing a new image
  if [[ "$lastshot" != "$lastsorted" ]]
  then
    # Make sure the image has changed enough to justify
    # a new munge
    munge=1

    if [ -n "$lastsorted" ]
    then
      changedpixels=0

      if [ -f $lastsorted ]
      then
        changedpixels=`compare -metric AE $lastsorted $lastshot null: 2>&1`
      fi

      if [ "$changedpixels" -lt "$MAX_CHANGED_PIXELS" ]
      then
        munge=0
      fi
    fi

    if [[ $munge == 1 ]]
    then
      filename=`basename $lastshot`
      pipenv run python sort_image.py $lastshot "A screenshot with pixels sorted by random criteria" "${filename:0:4}-${filename:4:2}-${filename:6:2} ${filename:8:2}:${filename:10:2}:${filename:12:2}"

      # Log the sorted file
      echo "$lastshot" > lastsorted.dat
    fi
  fi
fi
