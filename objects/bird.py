from typing import Tuple
import pygame
from pygame.sprite import AbstractGroup

from imgs.bird import DEFAULT_BIRD_SIZE, get_birds

BIRD_FRAME_LENGTH = 3

class Bird(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int], size: Tuple[int] = DEFAULT_BIRD_SIZE) -> None:
        super().__init__()
        self.position = position
        self.size = size
        bird_images = get_birds()
        
        self.images = [pygame.image.frombuffer(bird.tobytes(), bird.shape[:2][::-1], 'RGBA') for bird in bird_images]
        self.images.append(self.images[1])
        self.frame = 0
        
    def update(self) -> None:
        self.frame += 1

    @property
    def image(self):
        i = (self.frame // BIRD_FRAME_LENGTH) % len(self.images)
        return self.images[i]