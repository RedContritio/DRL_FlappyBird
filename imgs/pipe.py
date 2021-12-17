import cv2
import numpy as np

from numpy.lib import math

PIPE_HAT_HEIGHT = 20
PIPE_HIGHLIGHT_HAT_POSITION = 1 - 0.8 
PIPE_HIGHLIGHT_VALUE = [221, 246, 129, 255]
PIPE_LOWLIGHT_VALUE = [85, 131, 33, 255]

mix = lambda p, l, r: r * p + l * (1 - p)
negone = lambda p: 1 - p

def make_pipe_hat(height: int, width: int) -> np.array:
    img = np.zeros((min(height, PIPE_HAT_HEIGHT), width, 4), dtype=np.ubyte)

    jsplit = int(width * PIPE_HIGHLIGHT_HAT_POSITION)
    for j in range(jsplit):
        p = j / width / PIPE_HIGHLIGHT_HAT_POSITION
        img[:, j] = [mix(math.pow(p, 1.5), PIPE_LOWLIGHT_VALUE[i], PIPE_HIGHLIGHT_VALUE[i]) for i in range(len(PIPE_HIGHLIGHT_VALUE))] 

    for j in range(jsplit, width):
        p = negone(j /  width) / negone(PIPE_HIGHLIGHT_HAT_POSITION)
        img[:, j] = [mix(math.pow(p, 1.5), PIPE_LOWLIGHT_VALUE[i], PIPE_HIGHLIGHT_VALUE[i]) for i in range(len(PIPE_HIGHLIGHT_VALUE))] 

    img[:, 0, :3] = img[:, -1, :3] = 0
    img[0, :, :3] = img[-1, :, :3] = 0
    return img

def make_pipe_body(height: int, width: int) -> np.array:
    img = np.zeros((height, width, 4), dtype=np.ubyte)
    img[:, :] = 0

    margin = 0.08
    bl, br = int(width * margin), int(width * (1 - margin))

    highp = int(width * ((1 - 2 * margin) * PIPE_HIGHLIGHT_HAT_POSITION + margin))

    for j in range(bl, highp):
        p = (j - bl) / (highp - bl)
        img[:, j] = [mix(math.pow(p, 1.5), PIPE_LOWLIGHT_VALUE[i], PIPE_HIGHLIGHT_VALUE[i]) for i in range(len(PIPE_HIGHLIGHT_VALUE))] 

    for j in range(highp, br):
        p = negone((j - highp) / (br - highp))
        img[:, j] = [mix(math.pow(p, 1.5), PIPE_LOWLIGHT_VALUE[i], PIPE_HIGHLIGHT_VALUE[i]) for i in range(len(PIPE_HIGHLIGHT_VALUE))] 

    img[:, bl] = img[:, br] = [0, 0, 0, 255]

    return img

def make_pipe(height: int, width: int, upward: bool = True):
    img = np.zeros((height, width, 4), dtype=np.ubyte)
    img[:] = 255

    hat = make_pipe_hat(height, width)
    body = make_pipe_body(height - hat.shape[0], width)

    if upward:
        img[:hat.shape[0]] = hat
        img[hat.shape[0]:] = body
    else:
        img[:body.shape[0]] = body
        img[body.shape[0]:] = hat

    return img

