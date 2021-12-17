import pygame
from objects.ground import Ground

class Background(pygame.sprite.Group):
    def __init__(self, width: int) -> None:
        super().__init__()

        self.ground = Ground(width)
        self.add(self.ground)
        self.frame = 0

    def update(self, curx: int):
        self.ground.update(curx)
        self.frame += 1
