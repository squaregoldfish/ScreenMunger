import numpy as np
import cv2
from math import floor


def average_pixel(image):
    return np.average(image, axis=(0, 1))


class FrameColours:
    def __init__(self, frame_count):
        self.frames = frame_count
        self.pixels = np.zeros((1, frame_count, 3), np.uint8)

    def set_frame(self, frame, colour):
        self.pixels[:, frame, :] = colour

    def write_image(self, height, file):
        # Height is 1/8th of width
        ratio_height = self.frames / 8

        # Ratio to get image of correct aspect ratio to 720px
        final_height_ratio = 1 if ratio_height < 720 else 720 / ratio_height

        image = cv2.resize(self.pixels, (floor(self.frames * final_height_ratio), 720), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(file, image)

