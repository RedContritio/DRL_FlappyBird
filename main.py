import pygame
import sys
from game import Game
from objects.background import BACKGROUND_COLOR, Background

from objects.bird import Bird
from objects.pipe import Pipe

pygame.init()
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = (640, 480)
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

game = Game(WINDOW_SIZE)

# pipes = [Pipe((0, 0), (60, 100))]
bird = Bird(game.bird_position)
background = Background(WINDOW_SIZE)
curx = 0

while True:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.click()

    curx += 1
    game.update()
    bird.update(game)
    background.update(game)

    screen.fill(BACKGROUND_COLOR)
    background.draw(screen)
    screen.blit(bird.image, bird.position)
    # for p in pipes:
        # screen.blit(p.image, p.position)
    pygame.display.flip()

pygame.quit()