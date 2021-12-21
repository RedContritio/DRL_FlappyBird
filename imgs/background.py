import cv2
import numpy as np
import math

BASE_UNIT_WIDTH = 24

def get_base(width: int):
    img = cv2.imread('assets/sprites/base.png', -1)

    realwidth = math.ceil(width / BASE_UNIT_WIDTH) * BASE_UNIT_WIDTH

    nimg = np.zeros((img.shape[0], realwidth, 4), dtype=np.ubyte)

    fr = min(img.shape[1], nimg.shape[1])
    nimg[:, :fr] = img[:, :fr]
    
    for i in range(realwidth // img.shape[1]):
        nimg[:, i * img.shape[1]: (i + 1) * img.shape[1]] = img

    
    if realwidth % img.shape[1] != 0:
        p = realwidth - img.shape[1] * (realwidth // img.shape[1])
        l = realwidth - p
        nimg[:, p:] = img[:, :l]


    return nimg