#!/bin/bash
do_capture=1

# See if xscreensaver is installed.
# If so, and if the screensaver is running,
# we don't capture.

if command -v xscreensaver-command &> /dev/null
then
    status=`xscreensaver-command -time`
    case "$status" in
        *non-blanked*)
            do_capture=1
            ;;
        *"no saver status"*)
            do_capture=1
            ;;
        *)
            do_capture=0
    esac
else
    do_capture=1
fi


if [ $do_capture -eq 1 ]
then
    dir="`dirname $0`/uploads/`date '+%Y%m%d'`"

    if [ ! -d $dir ]
    then
        mkdir -p $dir
    fi

    DISPLAY=:0 scrot $dir/`date '+%Y%m%d%H%M'`00.png
fi

