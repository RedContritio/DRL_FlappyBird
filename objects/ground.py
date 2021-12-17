import pygame

from imgs.background import BASE_UNIT_WIDTH, get_base

class Ground(pygame.sprite.Sprite):
    def __init__(self, width: int) -> None:
        super().__init__()

        image = get_base(width + BASE_UNIT_WIDTH)
        self.image = pygame.image.frombuffer(image.tobytes(), image.shape[:2][::-1], 'RGBA')
        self.rect = (0, 0, image.shape[1], image.shape[0])
        self.curx = 0
        
    def update(self, x: int):
        self.curx = x
        lx = -(self.curx % BASE_UNIT_WIDTH)
        self.rect = (lx, 0, self.rect[2], self.rect[3])
    