from typing import Tuple
import pygame
import math
from pygame.sprite import AbstractGroup
from game import Game

from imgs.bird import DEFAULT_BIRD_SIZE, get_birds

BIRD_FRAME_LENGTH = 2

class Bird(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int], size: Tuple[int] = DEFAULT_BIRD_SIZE) -> None:
        super().__init__()
        self.position = position
        self.speed = []
        self.size = size
        bird_images = get_birds()
        print(bird_images[0])
        
        self.images = [pygame.image.frombuffer(bird.tobytes(), bird.shape[:2][::-1], 'RGBA') for bird in bird_images]
        self.images.append(self.images[1])
        self.angle = 0
        self.frame = 0
        
    def update(self, game: Game) -> None:
        self.position = game.bird_position
        self.speed = game.bird_speed
        self.angle = math.atan2(self.speed[1], self.speed[0] * 2) # less rotate angle
        if game.running:
            if self.speed[1] < 0:
                self.frame += 1
            else:
                self.frame = 0

    @property
    def image(self):
        i = (self.frame // BIRD_FRAME_LENGTH) % len(self.images)
        source = self.images[1] if self.speed[1] >= 0 else self.images[i]
        dst = pygame.transform.rotate(source, -self.angle / math.pi * 180)
        return dst