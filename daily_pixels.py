import argparse
import os
import tempfile
import re
import cv2
import FrameColours
from multiprocessing.managers import BaseManager
from multiprocessing import Pool
from itertools import repeat
from postimage import post_image


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
parser.add_argument('toot', help='Toot text')
parser.add_argument('alt', help='Alt text')
args = parser.parse_args()

file_prefix = os.path.basename(args.image_dir)

BaseManager.register('FrameColours', FrameColours.FrameColours)
manager = BaseManager()
manager.start()
average_pixels = manager.FrameColours(1440)

pool = Pool()
pool.starmap(process_frame, zip(os.listdir(args.image_dir), repeat(average_pixels)))

temp_file = f'{os.path.join(tempfile.gettempdir(), args.toot)}.png'
average_pixels.write_image(720, temp_file)

post_image(temp_file, args.alt, args.toot)

os.remove(temp_file)
