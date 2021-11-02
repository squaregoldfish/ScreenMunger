import argparse
import os
import re
import cv2
import FrameColours
from multiprocessing.managers import BaseManager
from multiprocessing import Pool
from itertools import repeat


def get_minute(file_name):
    p = re.compile('.*([0-9][0-9])([0-9][0-9])[0-9][0-9]\\.png$')
    m = p.match(file_name)
    hour = int(m.group(1))
    minute = int(m.group(2))
    return (hour * 60) + minute


def get_average_pixel(img_file):
    image = cv2.imread(img_file)
    return FrameColours.average_pixel(image)


def process_frame(frame_file, avg_pixels):
    minute_of_day = get_minute(frame_file)
    pixel = get_average_pixel(os.path.join(args.image_dir, frame_file))
    avg_pixels.set_frame(minute_of_day, pixel)


parser = argparse.ArgumentParser(description='Generate an average pixel image for a day\'s worth of screen grabs')
parser.add_argument('image_dir', help='Directory containing screen grabs')
parser.add_argument('out_file', help='Output file')
args = parser.parse_args()

file_prefix = os.path.basename(args.image_dir)

BaseManager.register('FrameColours', FrameColours.FrameColours)
manager = BaseManager()
manager.start()
average_pixels = manager.FrameColours(1440)

pool = Pool()
pool.starmap(process_frame, zip(os.listdir(args.image_dir), repeat(average_pixels)))

average_pixels.write_image(720, args.out_file)
