import numpy as np
import cv2


def average_pixel(image):
    return np.average(image, axis=(0, 1))


class FrameColours:
    def __init__(self, frame_count):
        self.frames = frame_count
        self.pixels = np.zeros((1, frame_count, 3), np.uint8)

    def set_frame(self, frame, colour):
        self.pixels[:, frame, :] = colour

    def write_image(self, height, file):
        image = cv2.resize(self.pixels, (self.frames, height), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(file, image)

