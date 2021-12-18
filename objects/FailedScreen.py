from typing import Tuple
import pygame

from imgs.failed import make_Failed

class FailedScreen(pygame.sprite.Sprite):
    def __init__(self, window_size: Tuple[int], score: int, best_score: int = 0) -> None:
        super().__init__()

        image = make_Failed(window_size[::-1], score, best_score)
        self.image = pygame.image.frombuffer(image.tobytes(), window_size, 'RGBA')
        self.position = (0, 0)