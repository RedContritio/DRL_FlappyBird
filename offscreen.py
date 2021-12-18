from game import Game
import numpy as np
from config import WINDOW_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from imgs.background import BASE_UNIT_WIDTH, get_base
from imgs.scoreboard import make_scoreboard
from objects.background import BACKGROUND_COLOR
from objects.ground import GROUND_HEIGHT

ground = get_base(WINDOW_WIDTH + BASE_UNIT_WIDTH)

def mix(background, foreground):
    alpha_back = background[:,:,3] / 255.
    alpha_fore = foreground[:,:,3] / 255.

    for c in range(3):
        background[:,:,c] = np.ubyte(alpha_fore * foreground[:,:,c] + alpha_back * background[:,:,c] * (1 - alpha_fore))
    
    background[:,:,3] = np.ubyte((1 - (1 - alpha_fore) * (1 - alpha_back)) * 255)

def render(game: Game):
    img = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 4), dtype=np.ubyte)
    img[:, :, :3] = BACKGROUND_COLOR
    img[:, :, 3] = 255

    curx = game.camera_rect[0]
    ground_left = (curx % BASE_UNIT_WIDTH)
    mix(img[WINDOW_HEIGHT - GROUND_HEIGHT:], ground[:GROUND_HEIGHT, ground_left:ground_left + WINDOW_WIDTH])

    scoreboard = make_scoreboard(WINDOW_SIZE[::-1], game.score, game.best_score)
    mix(img, scoreboard)

    return img