import math
from typing import List, Tuple
import cv2
from game import AbstractPipe, Game
import numpy as np
from config import WINDOW_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from imgs.background import BASE_UNIT_WIDTH, get_base
from imgs.bird import get_birds
from imgs.pipe import make_pipe
from imgs.scoreboard import make_scoreboard
from objects.background import BACKGROUND_COLOR
from objects.bird import BIRD_FRAME_LENGTH
from objects.ground import GROUND_HEIGHT

ground = get_base(WINDOW_WIDTH + BASE_UNIT_WIDTH)
raw_birds = get_birds()

def mix(background, foreground):
    '''
    mix foreground image to background image, modify background inplace
    '''
    alpha_back = background[:,:,3] / 255.
    alpha_fore = foreground[:,:,3] / 255.

    for c in range(3):
        background[:,:,c] = np.ubyte(alpha_fore * foreground[:,:,c] + alpha_back * background[:,:,c] * (1 - alpha_fore))
    
    background[:,:,3] = np.ubyte((1 - (1 - alpha_fore) * (1 - alpha_back)) * 255)

def rotate(src: np.array, angle: float):
    image_center = tuple(np.array(src.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)
    result = cv2.warpAffine(src, rot_mat, src.shape[1::-1], flags = cv2.INTER_LINEAR)
    return result

def getRenderRect(back_rect: List[int], fore_rect: List[int]):
    bl, bt = back_rect[:2]
    br, bb = [back_rect[i] + back_rect[i + 2] for i in range(2)]
    fl, ft = fore_rect[:2]
    fr, fb = [fore_rect[i] + fore_rect[i + 2] for i in range(2)]
    
    xl, xr = max(bl, fl), min(br, fr)
    yt, yb = max(bt, ft), min(bb, fb)

    return ([xl, yt, max(0, xr - xl), max(0, yb - yt)])
    
def renderPipe(img, p: AbstractPipe, game: Game):
    imgbox = [0, 0, img.shape[1], img.shape[0]]
    curx = game.camera_rect[0]
    upos = list(p.upperPosition)
    upos[0] -= curx
    uimg = make_pipe(p.upperSize[1], p.upperSize[0], False)
    
    ubox = [upos[0], upos[1], uimg.shape[1], uimg.shape[0]]
    ul, ut, uw, uh = getRenderRect(imgbox, ubox)
    ur, ub = ul + uw, ut + uh

    if ubox[2] > 0 and ubox[3] > 0:
        mix(img[ut: ub, ul: ur], uimg[ut - upos[1]: ub - upos[1], ul - upos[0]: ur - upos[0]])

    lpos = list(p.lowerPosition)
    lpos[0] -= curx
    limg = make_pipe(p.lowerSize[1], p.lowerSize[0])

    lbox = [lpos[0], lpos[1], limg.shape[1], limg.shape[0]]
    ll, lt, lw, lh = getRenderRect(imgbox, lbox)
    lr, lb = ll + lw, lt + lh

    if lbox[2] > 0 and lbox[3] > 0:
        mix(img[lt: lb, ll: lr], limg[lt - lpos[1]: lb - lpos[1], ll - lpos[0]: lr - lpos[0]])

def renderbird(img, game: Game):
    if not hasattr(renderbird, 'frame'):
        renderbird.frame = 0
    if game.bird_speed[1] < 0:
        renderbird.frame += 1
    else:
        renderbird.frame = 0
    i = (renderbird.frame // BIRD_FRAME_LENGTH) % len(raw_birds)
    source = raw_birds[i] if game.running and game.bird_speed[1] < 0 else raw_birds[1]
    dst = rotate(source, -game.bird_rotate / math.pi * 180)
    h, w = dst.shape[:2]
    x, y = game.bird_position
    x, y = int(x), int(y)
    mix(img[y:y+h, x:x+w], dst)

def render(game: Game):
    img = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 4), dtype=np.ubyte)
    img[:, :, :3] = BACKGROUND_COLOR
    img[:, :, 3] = 255

    curx = game.camera_rect[0]

    for p in game.pipes:
        renderPipe(img, p, game)
    
    ground_left = (curx % BASE_UNIT_WIDTH)
    mix(img[WINDOW_HEIGHT - GROUND_HEIGHT:], ground[:GROUND_HEIGHT, ground_left:ground_left + WINDOW_WIDTH])

    scoreboard = make_scoreboard(WINDOW_SIZE[::-1], game.score, game.best_score)
    mix(img, scoreboard)

    renderbird(img, game)

    return img