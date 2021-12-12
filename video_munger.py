import argparse
import os
import tempfile
from math import floor
import FrameColours
from multiprocessing.managers import BaseManager
from multiprocessing import Pool
from itertools import repeat
from postimage import post_image
from moviepy.editor import VideoFileClip
import numpy as np
from io import BytesIO


parser = argparse.ArgumentParser(description='Generate an average pixel image for each frame of a video')
parser.add_argument('video', help='Video file')
args = parser.parse_args()

video_clip = VideoFileClip(args.video)

extract_frames = np.arange(0, video_clip.duration, 0.1)
frame_count = len(extract_frames)
output = FrameColours.FrameColours(frame_count)

current_frame = 0
for frame in extract_frames:
    frame_jpg = BytesIO()
    output.set_frame(current_frame, FrameColours.average_pixel(video_clip.get_frame(frame)))
    current_frame += 1

output.write_image(floor(frame_count / 8), os.path.join(tempfile.gettempdir(), 'frames.png'))

#
# post_image(temp_file, args.alt, args.toot)
#
# os.remove(temp_file)
