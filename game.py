from typing import Tuple

BIRD_LEFT_POSITION = 0.2
BIRD_RIGHT_POSITION = 0.5
BIRD_SPEED = 3
BIRD_CLICK_SPEED = -4
WORLD_GRAVITY = 0.3

class Game:
    def __init__(self, window_size: Tuple[int]) -> None:
        self.bird_speed = [BIRD_SPEED, 0]
        self.bird_xrange = [int(BIRD_LEFT_POSITION * window_size[0]), int(BIRD_RIGHT_POSITION * window_size[0])]
        self.bird_world_position = [0, window_size[1] // 2]
        self.camera_rect = [0, 0, window_size[0], window_size[1]]
        self.fitCamera()

    def fitCamera(self):
        if self.bird_world_position[0] < self.camera_rect[0] + self.bird_xrange[0]:
            self.camera_rect[0] = self.bird_world_position[0] - self.bird_xrange[0]
        elif self.bird_world_position[0] > self.camera_rect[0] + self.bird_xrange[1]:
            self.camera_rect[0] = self.bird_world_position[0] - self.bird_xrange[1]

    def update(self):
        for i in range(2):
            self.bird_world_position[i] += self.bird_speed[i]
        self.bird_speed[1] += WORLD_GRAVITY

        self.fitCamera()
    
    @property
    def bird_position(self):
        return (self.bird_world_position[0] - self.camera_rect[0], self.bird_world_position[1] - self.camera_rect[1])

    def click(self):
        self.bird_speed[1] = BIRD_CLICK_SPEED
        
