import argparse
import os
from math import floor
import FrameColours
from moviepy.editor import VideoFileClip
import numpy as np
from awesome_progress_bar import ProgressBar

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

bar = ProgressBar(frame_count, prefix=title, use_spinner=False, use_eta=True)
current_frame = 0
for frame in extract_frames:
    output.set_frame(current_frame, FrameColours.average_pixel(video_clip.get_frame(frame), True))
    bar.iter()
    current_frame += 1

output.write_image(floor(frame_count / 8), os.path.join(OUT_DIR, f'{title}.png'))

if args.video.startswith('YouTube'):
    delete_file = input('Delete source video file? ')
    if delete_file.lower() == 'y':
        os.remove(args.video)