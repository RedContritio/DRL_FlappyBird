from typing import Tuple
import pygame

from imgs.background import BASE_UNIT_WIDTH, get_base

GROUND_HEIGHT = 60

class Ground(pygame.sprite.Sprite):
    def __init__(self, window_size: Tuple[int]) -> None:
        super().__init__()

        image = get_base(window_size[0] + BASE_UNIT_WIDTH)
        self.image = pygame.image.frombuffer(image.tobytes(), image.shape[:2][::-1], 'RGBA')
        self.rect = (0, window_size[1] - GROUND_HEIGHT, image.shape[1], image.shape[0])
        self.curx = 0
        
    def update(self, x: int):
        self.curx = x
        lx = -(self.curx % BASE_UNIT_WIDTH)
        self.rect = (lx, self.rect[1], self.rect[2], self.rect[3])
    