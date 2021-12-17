from typing import Tuple
import pygame
from game import Game
from objects.ground import Ground

class Background(pygame.sprite.Group):
    def __init__(self, window_size: Tuple[int]) -> None:
        super().__init__()

        self.ground = Ground(window_size)
        self.add(self.ground)
        self.frame = 0

    def update(self, game: Game):
        self.ground.update(game.camera_rect[0])
        self.frame += 1
