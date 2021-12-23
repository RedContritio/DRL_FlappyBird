#!/data/user18302289/anaconda3/envs/cvDQN/bin/python3.6
# use a dummy video device
import os
from typing import List
# os.environ["SDL_VIDEODRIVER"] = "dummy"
# os.environ['CUDA_VISIBLE_DEVICES'] = "0"
import cv2
import sys
from network.BrainDQN_Nature import BrainDQN
from game import PIPE_SAFE_MARGIN, Game, getRandomSeed
import numpy as np
from config import WINDOW_HEIGHT, WINDOW_SIZE
from offscreen import render

# get_seed = lambda: 'ZdfkR9jzpSli7uVt'
# get_seed = lambda: 'b5gMnJN0EHFKQiez'
get_seed = getRandomSeed 

_image_togray = lambda img: cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
_image_resize = lambda img: cv2.resize(img, (80, 80))
_image_threshold = lambda img: cv2.threshold(img, 1, 255, cv2.THRESH_BINARY)[1]
image_preprocess = lambda img: _image_threshold(_image_togray(_image_resize(img)))

def game_stepin(game: Game, action: List[int]):
    if action[0] < action[1]:
        game.action_fly()
    game.update()
    
    ret = [render(game), game.reward, game.dead]
    if game.dead:
        # game.reset(getRandomSeed())
        game.reset(get_seed())
        game.start()
        game.update()
        ret[1] = min(-1, game.reward)
    return tuple(ret)

# preprocess raw image to 80*80 gray image
def preprocess(observation):
	ob = image_preprocess(observation)
	return np.reshape(ob, (80, 80, 1))

def playFlappyBird():
	# Step 1: init BrainDQN
	actions = 2
	brain = BrainDQN(actions)
	# Step 2: init Flappy Bird Game
	game = Game(WINDOW_SIZE, True)
	game.reset(get_seed())
	game.start()
	game.update()
	# Step 3: play game
	# Step 3.1: obtain init state
	action0 = np.array([1,0])  # do nothing
	observation0, reward0, terminal = game_stepin(game, action0)
	observation0 = image_preprocess(observation0)
	brain.setInitState(observation0)

	# Step 3.2: run the game
	while True:
		action = brain.getAction()
		nextObservation,reward,terminal = game_stepin(game, action)
		nextObservation = preprocess(nextObservation)
		brain.setPerception(nextObservation,action,reward,terminal)

def main():
	playFlappyBird()

if __name__ == '__main__':
	main()
