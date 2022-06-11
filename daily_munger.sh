#!/bin/bash

#yesterday=`date -d 'yesterday' +%Y%m%d`
day_before_yesterday=`date -d '-2 day' +%Y%m%d`

#yesterday_long=`date -d 'yesterday' +%Y-%m-%d`

#pipenv run python daily_pixels.py ./uploads/$yesterday $yesterday_long "Image constructed by taking one screenshot per minute; each column of pixels is the average pixel colour of the screenshot."

rm -r ./uploads/$day_before_yesterday

