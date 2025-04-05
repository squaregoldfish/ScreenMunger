import argparse
import os
from math import floor
import FrameColours
from moviepy import VideoFileClip
import numpy as np
import cv2
from multiprocessing import cpu_count, shared_memory, Pool
from parallelbar.wrappers import add_progress
from parallelbar import progress_starmap

OUT_DIR='./uploads/video'

def average_frame(frame_time, frame_index):
    fc_shm = shared_memory.SharedMemory(name='fc_shm')
    fc = np.ndarray((frame_count, 3), dtype=np.uint8, buffer=fc_shm.buf)
    fc[frame_index] = FrameColours.average_pixel(video_clip.get_frame(frame_time), True)

    del fc
    fc_shm.close()


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

try:
    frame_colors = np.zeros((frame_count, 3))
    fc_shm = shared_memory.SharedMemory(name='fc_shm', create=True, size=frame_colors.nbytes)
    fc = np.ndarray(frame_colors.shape, dtype=np.uint8, buffer=fc_shm.buf)

    progress_starmap(average_frame, zip(extract_frames, range(frame_count)), total=frame_count, n_cpu=int(cpu_count() / 2))

    frame_colors[:] = fc[:]
    output = FrameColours.FrameColours(frame_count)
    output.set_frames(frame_colors)
    output.write_image(floor(frame_count / 8), os.path.join(OUT_DIR, f'{title}.jpg'))
finally:
    del frame_colors
    fc_shm.close()
    fc_shm.unlink()

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
