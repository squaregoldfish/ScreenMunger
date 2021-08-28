#!/bin/bash

dir="`dirname $0`/uploads/`date '+%Y%m%d'`"

if [ ! -d $dir ]
then
  mkdir -p $dir
fi

DISPLAY=:0 scrot $dir/`date '+%Y%m%d%H%M'`00.png

