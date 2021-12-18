from typing import Tuple
from imgs.bird import DEFAULT_BIRD_HEIGHT

from objects.ground import GROUND_HEIGHT

BIRD_LEFT_POSITION = 0.2
BIRD_RIGHT_POSITION = 0.5
BIRD_SPEED = 3
BIRD_CLICK_SPEED = -5
WORLD_GRAVITY = 0.4

GAME_STATE_INIT = 0
GAME_STATE_RUNNING = 1
GAME_STATE_END = 2

class Game:
    def __init__(self, window_size: Tuple[int]) -> None:
        self.window_size = window_size
        self.bird_xrange = [int(BIRD_LEFT_POSITION * window_size[0]), int(BIRD_RIGHT_POSITION * window_size[0])]
        self.status = GAME_STATE_INIT
        self.reset()
        self.pipes = []

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
            if self.checkCollision():
                self.status = GAME_STATE_END

        self.fitCamera()
    
    def reset(self):
        self.bird_speed = [BIRD_SPEED, 0]
        self.bird_world_position = [0, self.window_size[1] // 2]
        self.camera_rect = [0, 0, self.window_size[0], self.window_size[1]]
        self.fitCamera()

    @property
    def bird_position(self):
        return (self.bird_world_position[0] - self.camera_rect[0], self.bird_world_position[1] - self.camera_rect[1])

    def checkCollision(self):
        if self.bird_world_position[1] <= 0 or self.bird_world_position[1] + DEFAULT_BIRD_HEIGHT >= self.window_size[1] - GROUND_HEIGHT:
            return True

    def click(self):
        if self.status == GAME_STATE_RUNNING:
            if self.bird_speed[1] * BIRD_CLICK_SPEED < 0:
                self.bird_speed[1] = 0
            self.bird_speed[1] += BIRD_CLICK_SPEED
        if self.status == GAME_STATE_INIT:
            self.status = GAME_STATE_RUNNING
        if self.status == GAME_STATE_END:
            self.reset()
            self.status = GAME_STATE_INIT

    @property
    def running(self):
        return self.status == GAME_STATE_RUNNING
        
