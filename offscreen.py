from game import AbstractPipe, Game
import numpy as np
from config import WINDOW_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from imgs.background import BASE_UNIT_WIDTH, get_base
from imgs.pipe import make_pipe
from imgs.scoreboard import make_scoreboard
from objects.background import BACKGROUND_COLOR
from objects.ground import GROUND_HEIGHT

ground = get_base(WINDOW_WIDTH + BASE_UNIT_WIDTH)

def mix(background, foreground):
    '''
    mix foreground image to background image, modify background inplace
    '''
    alpha_back = background[:,:,3] / 255.
    alpha_fore = foreground[:,:,3] / 255.

    for c in range(3):
        background[:,:,c] = np.ubyte(alpha_fore * foreground[:,:,c] + alpha_back * background[:,:,c] * (1 - alpha_fore))
    
    background[:,:,3] = np.ubyte((1 - (1 - alpha_fore) * (1 - alpha_back)) * 255)

def renderPipe(img, p: AbstractPipe, game: Game):
    upos = p.upperPosition
    uimg = make_pipe(p.upperSize[1], p.upperSize[0], False)
    
    uw = min(p.upperSize[0], WINDOW_WIDTH - upos[0])
    uh = p.upperSize[1]
    if uw > 0:
        mix(img[:uh, upos[0]:upos[0] + uw], uimg[:, :uw])

    lpos = p.lowerPosition
    limg = make_pipe(p.lowerSize[1], p.lowerSize[0])

    lw = min(p.lowerSize[0], WINDOW_WIDTH - lpos[0])
    lh = p.lowerSize[1]
    if lw > 0:
        mix(img[lpos[1]:lpos[1]+lh, lpos[0]:lpos[0] + lw], limg[:lh, :lw])

def render(game: Game):
    img = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 4), dtype=np.ubyte)
    img[:, :, :3] = BACKGROUND_COLOR
    img[:, :, 3] = 255

    curx = game.camera_rect[0]

    scoreboard = make_scoreboard(WINDOW_SIZE[::-1], game.score, game.best_score)
    mix(img, scoreboard)

    for p in game.pipes:
        renderPipe(img, p, game)
    
    ground_left = (curx % BASE_UNIT_WIDTH)
    mix(img[WINDOW_HEIGHT - GROUND_HEIGHT:], ground[:GROUND_HEIGHT, ground_left:ground_left + WINDOW_WIDTH])

    return img