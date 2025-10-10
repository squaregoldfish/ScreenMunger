import argparse
import os
import random
from moviepy import VideoFileClip
import tempfile
import cv2
import PixelSorter
import math


OUT_DIR='./uploads/video'

parser = argparse.ArgumentParser(description='Munge a random frame from a video')
parser.add_argument('--no-swap', action='store_true', help='Do not allow the swap mode')
parser.add_argument('video', help='Video file')
args = parser.parse_args()

title = os.path.splitext(os.path.basename(args.video))[0]
print(f'Default title: {title}')
custom_title = input('Enter alternative title if desired: ').strip()
if custom_title != '':
    title = custom_title

video_clip = VideoFileClip(args.video)
frame_pos = random.uniform(0, video_clip.duration)
hours = math.floor(frame_pos / 3600)
minutes = math.floor((frame_pos - (hours * 3600)) / 60)
seconds = frame_pos - (hours * 3600) - (minutes * 60)
print(f'{hours}:{minutes:02d}:{seconds:05.2f}')
frame = video_clip.get_frame(frame_pos)
# Frame is RBG - needs to be RGB
frame = frame[...,::-1].copy()
temp_file = os.path.join(tempfile.gettempdir(), f'{title}.jpg')
cv2.imwrite(temp_file, frame)

if args.no_swap:
    sort_criteria = random.choice(['C', 'L', 'H', 'B'])
else:
    sort_criteria = random.choice(['C', 'L', 'H', 'B', 'FT', 'FL', 'S', 'ROT'])

sort_mode = random.choice(['S', 'M'])
direction = random.choice(['H', 'V'])
reverse = random.choice(['T', 'F'])

# Perform the sort
sorter = PixelSorter.PixelSorter(temp_file, os.path.join(OUT_DIR, f'{title}.jpg'), sort_criteria, sort_mode, direction, reverse)
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
