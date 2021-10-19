import argparse
import os
import re
import cv2
import FrameColours


def get_minute(file_name):
    p = re.compile('.*([0-9][0-9])([0-9][0-9])[0-9][0-9]\\.png$')
    m = p.match(file_name)
    hour = int(m.group(1))
    minute = int(m.group(2))
    return (hour * 60) + minute


def get_average_pixel(file):
    image = cv2.imread(file)
    return FrameColours.average_pixel(image)


parser = argparse.ArgumentParser(description='Generate an average pixel image for a day\'s worth of screen grabs')
parser.add_argument('image_dir', help='Directory containing screen grabs')
parser.add_argument('out_file', help='Output file')
args = parser.parse_args()

file_prefix = os.path.basename(args.image_dir)

average_pixels = FrameColours.FrameColours(1440)

for file in os.listdir(args.image_dir):
    minute_of_day = get_minute(file)
    pixel = get_average_pixel(os.path.join(args.image_dir, file))
    average_pixels.set_frame(minute_of_day, pixel)

average_pixels.write_image(1080, args.out_file)
