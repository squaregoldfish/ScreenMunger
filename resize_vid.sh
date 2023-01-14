infile=$1
outfile="`echo $infile|awk '{s=gensub(/ [^ ]*].webm/,"","g");print s}'`.mp4"

dimensions=`ffprobe -v error -show_entries stream=width,height -of csv=p=0:s=x "$infile"`

width=`echo $dimensions|awk '{s=gensub(/x.*/,"","g");print s}'`
height=`echo $dimensions|awk '{s=gensub(/.*x/,"","g");print s}'`

if [ $width -gt $height ]
then
  newsize="-2:720"
else
  newsize="720:-2"
fi

nice -n 10 ffmpeg-bar -i "$infile" -filter:v scale=$newsize -c:v libx264 -preset fast -crf 28 -r 24 -c:a copy "$outfile"

