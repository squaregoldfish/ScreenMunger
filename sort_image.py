"""
Sort an image and post it to Mastodon
"""
import argparse
import random
import tempfile
import os
from PixelSorter import PixelSorter
from postimage import post_image

# Command line parsing
parser = argparse.ArgumentParser(
    description='Sort an image and post it to Mastodon')
parser.add_argument('--no-swap', action='store_true', help='Do not allow the swap mode')
parser.add_argument('file', type=str, help='image file')
parser.add_argument('alt', type=str, help='alt text')
parser.add_argument('toot', type=str, help='toot text')
args = parser.parse_args()

# Choose random options for the sorter
if args.no_swap:
    sort_criteria = random.choice(['C', 'L', 'H', 'B', 'FT', 'FL'])
else:
    sort_criteria = random.choice(['C', 'L', 'H', 'B', 'FT', 'FL', 'S'])

sort_mode = random.choice(['S', 'M'])
direction = random.choice(['H', 'V'])
reverse = random.choice(['T', 'F'])

# Perform the sort
temp_file = os.path.join(tempfile.gettempdir(), f'{os.path.basename(args.file).split(".")[0]}.jpg')
sorter = PixelSorter.PixelSorter(args.file, temp_file, sort_criteria, sort_mode, direction, reverse)
sorter.pixel_sorter_middleware()

# Post the sorted image
post_image(temp_file, args.alt, args.toot)

# Tidy up
os.remove(temp_file)
