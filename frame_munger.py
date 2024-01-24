import argparse
import os
import random
from moviepy.editor import VideoFileClip
import tempfile
import cv2
from PixelSorter import PixelSorter
import math


OUT_DIR='./uploads/video'

parser = argparse.ArgumentParser(description='Generate an average pixel image for each frame of a video')
parser.add_argument('video', help='Video file')
args = parser.parse_args()

title = os.path.splitext(os.path.basename(args.video))[0]
print(f'Default title: {title}')
custom_title = input('Enter alternative title if desired: ').strip()
if custom_title != '':
    title = custom_title

video_clip = VideoFileClip(args.video)
frame = video_clip.get_frame(random.uniform(0, video_clip.duration))
# Frame is RBG - needs to be RGB
frame = frame[...,::-1].copy()
temp_file = os.path.join(tempfile.gettempdir(), f'{title}.png')
cv2.imwrite(temp_file, frame)

sort_criteria = random.choice(['C', 'L', 'H', 'B'])
sort_mode = random.choice(['S', 'M'])
direction = random.choice(['H', 'V'])
reverse = random.choice(['T', 'F'])

# Perform the sort
sorter = PixelSorter.PixelSorter(temp_file, os.path.join(OUT_DIR, f'{title}.png'), sort_criteria, sort_mode, direction, reverse)
sorter.pixel_sorter_middleware()

os.remove(temp_file)

vid = cv2.VideoCapture(args.video)
fps = vid.get(cv2.CAP_PROP_FPS)
if fps > 0:
    frame_count = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    length = (int(math.floor(frame_count / fps))) / 3600
    print(f'Video length: {length:.2f}')

if args.video.startswith('YouTube') or args.video.startswith('Vimeo'):
    size = os.path.getsize(args.video)
    if size >= 1073741824:
        gb = size / 1073741824
        print(f'{gb:.2f} Gb')
    else:
        mb = size / 1048576
        print(f'{mb:.2f} Mb')

    delete_file = input('Delete source video file? ')
    if delete_file.lower() == 'y':
        os.remove(args.video)
