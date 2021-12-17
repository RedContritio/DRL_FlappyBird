from typing import Tuple
import pygame
from objects.ground import Ground

class Background(pygame.sprite.Group):
    def __init__(self, window_size: Tuple[int]) -> None:
        super().__init__()

        self.ground = Ground(window_size)
        self.add(self.ground)
        self.frame = 0

    def update(self, curx: int):
        self.ground.update(curx)
        self.frame += 1
