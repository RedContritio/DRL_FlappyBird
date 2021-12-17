from typing import List, Tuple
import cv2

def make_green_box(size: Tuple[int]):
    return size[0] * size[1] * [0, 255, 0]


def get_green_box(size: Tuple[int] = (40, 40)) -> bytes:
    return bytes(make_green_box(size))
