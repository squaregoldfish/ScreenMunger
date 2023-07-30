import argparse
import os
from math import floor
import FrameColours
from moviepy.editor import VideoFileClip
import numpy as np
from tqdm import tqdm
import cv2

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

extract_frames = np.arange(0, floor(video_clip.duration), 0.1)
frame_count = len(extract_frames)
output = FrameColours.FrameColours(frame_count)

with tqdm(total=frame_count, desc=title, unit="frame", dynamic_ncols=True) as bar:
    current_frame = 0
    for frame in extract_frames:
        output.set_frame(current_frame, FrameColours.average_pixel(video_clip.get_frame(frame), True))
        bar.update()
        current_frame += 1

output.write_image(floor(frame_count / 8), os.path.join(OUT_DIR, f'{title}.png'))

vid = cv2.VideoCapture(args.video)
fps = vid.get(cv2.CAP_PROP_FPS)
if fps > 0:
    frame_count = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    length = (int(floor(frame_count / fps))) / 3600
    print(f'Video length: {length:.2f}')

if args.video.startswith('YouTube'):
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
