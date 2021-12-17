import pygame
import sys
from objects.background import Background

from objects.bird import Bird
from objects.pipe import Pipe

pygame.init()
size = WINDOW_WIDTH, WINDOW_HEIGHT = (640, 480)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# pipes = [Pipe((0, 0), (60, 100))]
bird = Bird((200, 200))
background = Background(WINDOW_WIDTH)
curx = 0

while True:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    curx += 1
    bird.update()
    background.update(curx)

    screen.fill((255, 255, 255))
    background.draw(screen)
    screen.blit(bird.image, bird.position)
    # for p in pipes:
        # screen.blit(p.image, p.position)
    pygame.display.flip()

pygame.quit()