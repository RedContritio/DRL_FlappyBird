from typing import Tuple
import pygame
from pygame.sprite import AbstractGroup

from imgs.pipe import make_pipe

class Pipe(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int], size: Tuple[int], upward: bool = True) -> None:
        super().__init__()
        self.position = position
        self.size = size
        pipe = make_pipe(size[1], size[0], upward)
        self.image = pygame.image.frombuffer(pipe.tobytes(), pipe.shape[:2][::-1], 'RGBA')