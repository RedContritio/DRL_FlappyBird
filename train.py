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
from config import WINDOW_SIZE
from offscreen import render

_image_togray = lambda img: cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
_image_resize = lambda img: cv2.resize(img, (80, 80))
_image_threshold = lambda img: cv2.threshold(img, 1, 255, cv2.THRESH_BINARY)[1]
image_preprocess = lambda img: _image_threshold(_image_togray(_image_resize(img)))

def game_stepin(game: Game, action: List[int]):
    if action[0] < action[1]:
        game.action_fly()
    game.update()
    ret = (render(game), game.bird_world_position[0] + game.score * PIPE_SAFE_MARGIN, game.dead)
    if game.dead:
        game.reset(getRandomSeed())
        game.start()
        game.update()
    return ret

# preprocess raw image to 80*80 gray image
def preprocess(observation):
	observation = cv2.cvtColor(cv2.resize(observation, (80, 80)), cv2.COLOR_BGR2GRAY)
	ret, observation = cv2.threshold(observation,1,255,cv2.THRESH_BINARY)
	return np.reshape(observation,(80,80,1))

def playFlappyBird():
	# Step 1: init BrainDQN
	actions = 2
	brain = BrainDQN(actions)
	# Step 2: init Flappy Bird Game
	game = Game(WINDOW_SIZE, True)
	game.start()
	game.update()
	# Step 3: play game
	# Step 3.1: obtain init state
	action0 = np.array([1,0])  # do nothing
	observation0, reward0, terminal = game_stepin(game, action0)
	observation0 = cv2.cvtColor(cv2.resize(observation0, (80, 80)), cv2.COLOR_BGR2GRAY)
	ret, observation0 = cv2.threshold(observation0,1,255,cv2.THRESH_BINARY)
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