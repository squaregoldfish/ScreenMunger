""" docstring """
import cv2
import numpy as np
from statistics import mean
from math import floor
from multiprocessing import shared_memory, Pool
from itertools import repeat


def get_pixel_hue(r, g, b):
    # TODO: fix
    # RuntimeWarning: invalid value encountered in double_scalars
    r /= 256.0
    g /= 256.0
    b /= 256.0
    mini, maxi = min(r, g, b), max(r, g, b)
    hue = 0.0

    if mini != maxi:
        if maxi == r:
            hue = ((g - b) * 60.0) / (maxi - mini)
        elif maxi == g:
            hue = (2 + (b-r) * 60.0) / (maxi - mini)
        elif maxi == b:
            hue = (4 + (r-g) * 60.0) / (maxi - mini)

    if hue > 0:
        return floor(hue)
    else:
        return floor(360 - hue)


def get_pixel_chr(r, g, b):
    return max(r, g, b) - min(r, g, b)    # chroma


def get_pixel_lum(r, g, b):         # luminance
    return r*0.3 + g*0.59 + b*0.11


def get_pixel_bri(r, g, b):         # brightness
    return round(mean([r, g, b]))


def __get_sorted__(temp, mode, rev_status):
    new_rgb_vector = []
    if mode == 'L':
        for i in range(0, np.shape(temp)[0]):
            new_rgb_vector.append(get_pixel_lum(temp[i][0], temp[i][1], temp[i][2]))
    elif mode == 'C':
        for i in range(0, np.shape(temp)[0]):
            new_rgb_vector.append(get_pixel_chr(temp[i][0], temp[i][1], temp[i][2]))
    elif mode == 'H':
        for i in range(0, np.shape(temp)[0]):
            new_rgb_vector.append(get_pixel_hue(temp[i][0], temp[i][1], temp[i][2]))
    elif mode == 'B':
        for i in range(0, np.shape(temp)[0]):
            new_rgb_vector.append(get_pixel_bri(temp[i][0], temp[i][1], temp[i][2]))
    return [rgb for sort_criteria, rgb in sorted(zip(new_rgb_vector, temp), reverse=rev_status)]


def process_row_smode(i, shape, cols, sort_criteria, reverse):
    b_shm = shared_memory.SharedMemory(name='b_shm')
    b = np.ndarray(shape, dtype=np.uint8, buffer=b_shm.buf)
    g_shm = shared_memory.SharedMemory(name='g_shm')
    g = np.ndarray(shape, dtype=np.uint8, buffer=g_shm.buf)
    r_shm = shared_memory.SharedMemory(name='r_shm')
    r = np.ndarray(shape, dtype=np.uint8, buffer=r_shm.buf)

    zipped = list(zip(r[i, ...][:cols], g[i, ...][:cols], b[i, ...][:cols]))
    temp = list(zipped[:])
    sorted_data = __get_sorted__(temp, sort_criteria, reverse)

    r[i, ...][:cols] = np.array([r for r, g, b in sorted_data])
    g[i, ...][:cols] = np.array([g for r, g, b in sorted_data])
    b[i, ...][:cols] = np.array([b for r, g, b in sorted_data])

    del b
    b_shm.close()
    del g
    g_shm.close()
    del r
    r_shm.close()

def process_row_mmode(i, shape, half_cols, sort_criteria, reverse):
    b_shm = shared_memory.SharedMemory(name='b_shm')
    b = np.ndarray(shape, dtype=np.uint8, buffer=b_shm.buf)
    g_shm = shared_memory.SharedMemory(name='g_shm')
    g = np.ndarray(shape, dtype=np.uint8, buffer=g_shm.buf)
    r_shm = shared_memory.SharedMemory(name='r_shm')
    r = np.ndarray(shape, dtype=np.uint8, buffer=r_shm.buf)

    # Pull out the RGB values for the columns we're using (every other column)
    zipped = list(zip(r[i, ...][::2], g[i, ...][::2], b[i, ...][::2]))
    temp = list(zipped[:])

    # Sort the data
    sorted_data = __get_sorted__(temp, sort_criteria, reverse)

    # Reconstruct the pixels
    r[i, ...][:half_cols] = np.array([r for r, g, b in sorted_data])
    g[i, ...][:half_cols] = np.array([g for r, g, b in sorted_data])
    b[i, ...][:half_cols] = np.array([b for r, g, b in sorted_data])

    # The right hand side is the flip of the left hand side
    r[i, ...][half_cols:] = r[i, ...][:half_cols][::-1]
    g[i, ...][half_cols:] = g[i, ...][:half_cols][::-1]
    b[i, ...][half_cols:] = b[i, ...][:half_cols][::-1]

    del b
    b_shm.close()
    del g
    g_shm.close()
    del r
    r_shm.close()


class ImageFeatureVector(object):
    """ docstring """
    def __init__(self, img_name, dest_img_path, sort_criteria, sort_mode, direction, reverse):
        self.img_name = img_name
        self.dest_img_path = dest_img_path
        self.sort_criteria = sort_criteria
        self.sort_mode = sort_mode
        self.direction = direction
        self.reverse = reverse
        self.pixel_data = None
        self.criteria_data = None
        self.img = None
        self.COLS = -1
        self.ROWS = -1
        
        # These will be shared memory arrays
        self.r = None
        self.r_shm = None
        self.g = None
        self.g_shm = None
        self.b = None
        self.b_shm = None

        self.channel_shape = None

        self.__process_img__()

    def get_color_channel(self):
        """ docstring """
        return self.r, self.g, self.b

    def __process_img__(self):
        """
        This is a helper method that is used to read in the data of the source image. This method
        gets all the pixel data of the source image to be edited.
        """
        self.img = cv2.imread(self.img_name)

        # Make sure we have an even number of rows and cols
        if np.shape(self.img)[0] % 2 == 1:
            self.img = np.delete(self.img, 0, axis=0)

        if np.shape(self.img)[1] % 2 == 1:
            self.img = np.delete(self.img, 0, axis=1)

        # If we're doing Vertical, rotate the image by 90 degrees
        if self.direction == 'V':
            self.img = cv2.rotate(self.img, cv2.ROTATE_90_CLOCKWISE)

        original_image = self.img.copy()
        original_image[:, :, 0] = self.img[:, :, 2]
        original_image[:, :, 2] = self.img[:, :, 0]
        self.COLS = self.get_no_cols()
        self.ROWS = self.get_no_rows()
        b, g, r = cv2.split(self.img)
        
        try:
            self.b_shm = shared_memory.SharedMemory(name='b_shm', create=True, size=b.nbytes)
            self.b = np.ndarray(b.shape, dtype=b.dtype, buffer=self.b_shm.buf)
            self.b[:] = b[:]
            self.channel_shape = b.shape

            self.g_shm = shared_memory.SharedMemory(name='g_shm', create=True, size=g.nbytes)
            self.g = np.ndarray(g.shape, dtype=g.dtype, buffer=self.g_shm.buf)
            self.g[:] = g[:]

            self.r_shm = shared_memory.SharedMemory(name='r_shm', create=True, size=r.nbytes)
            self.r = np.ndarray(r.shape, dtype=r.dtype, buffer=self.r_shm.buf)
            self.r[:] = r[:]

            if self.sort_mode == 'S':
                with Pool() as pool:
                    pool.starmap(process_row_smode,
                        zip(range(np.shape(self.b)[0]), repeat(self.channel_shape), repeat(self.COLS), repeat(self.sort_criteria), repeat(self.reverse)))
            else:
                half_cols = int(self.COLS / 2)
                with Pool() as pool:
                    pool.starmap(process_row_mmode,
                        zip(range(np.shape(self.b)[0]), repeat(self.channel_shape), repeat(half_cols), repeat(self.sort_criteria), repeat(self.reverse)))

            final_image = cv2.merge((self.b, self.g, self.r))

            # If we're doing Vertical, rotate the image back
            if self.direction == 'V':
                final_image = cv2.rotate(final_image, cv2.ROTATE_90_COUNTERCLOCKWISE)

            cv2.imwrite(self.dest_img_path, final_image, [cv2.IMWRITE_JPEG_QUALITY, 90])
        finally:
            # Release shared memory
            del self.b
            self.b_shm.close()
            self.b_shm.unlink()
            del self.g
            self.g_shm.close()
            self.g_shm.unlink()
            del self.r
            self.r_shm.close()
            self.r_shm.unlink()

    def get_no_rows(self):
        return self.img.shape[0]

    def get_no_cols(self):
        return self.img.shape[1]

    def is_img_clr(self):
        return self.img.shape[2] != 0

    def get_criteria_data(self):
        return self.criteria_data

    def get_pixel_data(self):
        """
        get the data for individual pixels, the return type of this method is a length
        3 turple that has individual pixel RGB data. NOTE: these are actually the original
        pixel data of the image that was read from the source image to be edited
        """
        return self.pixel_data

    def get_img_destination_path(self):
        """
        returns the destination or path of the resulting image, that has been sorted.
        """
        return self.dest_img_path

    def get_image_name(self):
        """
        returns the original image name that was being sorted or that was being edited.
        """
        return self.img_name
