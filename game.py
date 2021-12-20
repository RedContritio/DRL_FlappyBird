import math
import os
import re
from typing import Tuple

import numpy
from imgs.bird import DEFAULT_BIRD_HEIGHT, DEFAULT_BIRD_WIDTH
from imgs.pipe import PIPE_HAT_HEIGHT
import random

import time
from objects.ground import GROUND_HEIGHT
from prng import PRNG

BIRD_LEFT_POSITION = 0.2
# BIRD_RIGHT_POSITION = 0.5
BIRD_RIGHT_POSITION = 0.2
BIRD_SPEED = 3
BIRD_CLICK_SPEED = -5
WORLD_GRAVITY = 0.4

GAME_STATE_INIT = 0
GAME_STATE_RUNNING = 1
GAME_STATE_END = 2

PIPE_WIDTH = 60
PIPE_SPACING = 120

PIPE_SAFE_MARGIN = (PIPE_WIDTH + PIPE_SPACING)

PIPE_INTERVAL_MIN_HEIGHT = 70

# less means harder
GAME_DIFFICULT = 1.8

class AbstractPipe:
    g_id = 0

    def __init__(self, x: int, interval_y: int, interval_height: int, window_height: int) -> None:
        self.id = AbstractPipe.g_id
        AbstractPipe.g_id += 1

        self.width = PIPE_WIDTH
        self.x = x
        self.interval_y = interval_y
        self.interval_height = interval_height
        self.window_height = window_height

    @property
    def upperPosition(self):
        return (self.x, 0)
    
    @property
    def upperSize(self):
        return (self.width, self.interval_y)
    
    @property
    def lowerPosition(self):
        return (self.x, self.interval_y + self.interval_height)
    
    @property
    def lowerSize(self):
        return (self.width, self.window_height - self.lowerPosition[1])

    @property
    def right(self):
        return self.x + self.width

    def hit(self, y: int):
        if y < self.interval_y or y >= self.interval_y + self.interval_height:
            return True
        return False


def getRandomSeed():
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 16))

class Game:
    def __init__(self, window_size: Tuple[int], replay_flag: bool = False) -> None:
        self.window_size = window_size
        self.bird_xrange = [int(BIRD_LEFT_POSITION * window_size[0]), int(BIRD_RIGHT_POSITION * window_size[0])]
        self.score = 0
        self.best_score = 0
        self.operations = []
        self.prng = PRNG()
        self.replay_flag = replay_flag
        self.reset()

    def fitCamera(self):
        if self.bird_world_position[0] < self.camera_rect[0] + self.bird_xrange[0]:
            self.camera_rect[0] = self.bird_world_position[0] - self.bird_xrange[0]
        elif self.bird_world_position[0] > self.camera_rect[0] + self.bird_xrange[1]:
            self.camera_rect[0] = self.bird_world_position[0] - self.bird_xrange[1]

    def update(self):
        if self.status == GAME_STATE_RUNNING:
            for i in range(2):
                self.bird_world_position[i] += self.bird_speed[i]
            self.bird_speed[1] += WORLD_GRAVITY
            self.bird_rotate = math.atan2(self.bird_speed[1], self.bird_speed[0] * 2) # less rotate angle
            passed_pipes = [p for p in self.pipes if p.right < self.bird_world_position[0]]
            if len(passed_pipes) > 0:
                self.score = passed_pipes[-1].id + 1
                if self.score > self.best_score:
                    self.best_score = self.score
            if self.checkCollision():
                self.status = GAME_STATE_END
                if len(self.operations) > 0:
                    self.saveOperations()
            self.operations.append(0)

        self.updatePipe()
        self.fitCamera()
    
    def reset(self, seed = getRandomSeed()):
        AbstractPipe.g_id = 0
        self.seed = seed
        self.prng.seed(self.seed)
        self.status = GAME_STATE_INIT
        self.operations = []
        self.score = 0
        self.bird_rotate = 0
        self.bird_speed = [BIRD_SPEED, 0]
        self.bird_world_position = [0, self.window_size[1] // 2]
        self.camera_rect = [0, 0, self.window_size[0], self.window_size[1]]
        self.pipes = [self.makeRandomPipe(self.bird_world_position[0] + PIPE_SAFE_MARGIN, self.window_size[1] - GROUND_HEIGHT, PIPE_INTERVAL_MIN_HEIGHT * GAME_DIFFICULT)]
        self.fitCamera()

    def updatePipe(self):
        l, r = self.camera_rect[0] - PIPE_SAFE_MARGIN, self.camera_rect[0] + self.camera_rect[2] + PIPE_SAFE_MARGIN
        self.pipes = [p for p in self.pipes if p.x >= l]
        last = self.pipes[-1]
        while last.x + (PIPE_WIDTH + PIPE_SPACING) < r:
            pipe = (self.makeRandomPipe(last.x + (PIPE_SPACING + PIPE_WIDTH), self.window_size[1] - GROUND_HEIGHT, PIPE_INTERVAL_MIN_HEIGHT * GAME_DIFFICULT))
            self.pipes.append(pipe)
            last = self.pipes[-1]

    def makeRandomPipe(self, x: int, full_height: int, expect_interval_height: int):
        h = int(self.prng.random(0.8, 1.2) * expect_interval_height)
        k = int(math.floor(self.prng.random(PIPE_HAT_HEIGHT, full_height - h - PIPE_HAT_HEIGHT)))
        return AbstractPipe(x, k, h, self.window_size[1])

    @property
    def bird_position(self):
        return (self.bird_world_position[0] - self.camera_rect[0], self.bird_world_position[1] - self.camera_rect[1])

    def checkCollision(self):
        bird_l, bird_r = self.bird_world_position[0], self.bird_world_position[0] + DEFAULT_BIRD_WIDTH
        bird_t, bird_b = self.bird_world_position[1], self.bird_world_position[1] + DEFAULT_BIRD_HEIGHT
        if bird_t <= 0 or bird_b >= self.window_size[1] - GROUND_HEIGHT:
            return True
        
        for p in self.pipes:
            if bird_r in range(p.x, p.right) or bird_l in range(p.x, p.right):
                if p.hit(bird_t) or p.hit(bird_b):
                    return True
        
        return False

    def action_fly(self):
        if self.bird_speed[1] * BIRD_CLICK_SPEED < 0:
            self.bird_speed[1] = 0
        self.bird_speed[1] += BIRD_CLICK_SPEED
        self.operations[-1] += 1

    def click(self):
        if self.status == GAME_STATE_RUNNING:
            self.action_fly()
        if self.status == GAME_STATE_INIT:
            self.start()
        if self.status == GAME_STATE_END:
            self.reset()
            self.status = GAME_STATE_INIT

    @property
    def ready(self):
        return self.status == GAME_STATE_INIT

    @property
    def running(self):
        return self.status == GAME_STATE_RUNNING
    
    @property
    def dead(self):
        return self.status == GAME_STATE_END

    def start(self):
        assert(self.status == GAME_STATE_INIT)
        self.status = GAME_STATE_RUNNING

    def saveOperations(self):
        timestr = time.strftime(f'%Y_%m_%d_%H_%M_%S__score__{self.score}', time.localtime())
        filename = f'{timestr}.log'
        dirpath = os.path.join('log', 'actions')
        if not os.path.exists(dirpath) or not os.path.isdir(dirpath):
            if not os.path.exists('log') or not os.path.isdir('log'):
                os.mkdir('log')
            os.mkdir(dirpath)
        if not self.replay_flag:
            with open(os.path.join(dirpath, filename), 'w') as f:
                print(self.seed, file=f)
                print(self.operations, file=f)
        else:
            print(self.operations)
        with open(os.path.join('log', 'scores.txt'), 'a') as f:
            print(timestr, file=f)
            print(f'{self.seed} {self.bird_world_position}', file=f)
