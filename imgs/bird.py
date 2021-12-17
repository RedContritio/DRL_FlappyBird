from typing import Tuple
import cv2
import numpy as np

DEFAULT_BIRD_SIZE = DEFAULT_BIRD_WIDTH, DEFAULT_BIRD_HEIGHT = 34, 24

def _get_bird(type: str, size: Tuple[int] = DEFAULT_BIRD_SIZE):
    raw_img = cv2.imread(f'assets/sprites/redbird-{type}.png', -1)
    img = np.zeros((raw_img.shape[0], raw_img.shape[1], 4), dtype=np.ubyte)

    img[:, :, :] = raw_img
    img[:, :, :3] = raw_img[:, :, -2::-1]

    target = cv2.resize(img, size)

    return target

def get_birds(size: Tuple[int] = DEFAULT_BIRD_SIZE):
    types = ['downflap', 'midflap', 'upflap']
    return [_get_bird(t, size) for t in types]