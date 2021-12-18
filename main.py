import pygame
import sys
from game import Game
from objects.FailedScreen import FailedScreen
from objects.background import BACKGROUND_COLOR, Background

from objects.bird import Bird
from objects.pipe import Pipe
from objects.scoreboard import ScoreBoard

pygame.init()
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = (640, 480)
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

game = Game(WINDOW_SIZE)

pipes = []
# pipes = [Pipe((0, 0), (60, 100))]
bird = Bird(game.bird_position)
background = Background(WINDOW_SIZE)
failed = None
scoreboard = ScoreBoard(WINDOW_SIZE, 0)

def getUpperPipe(p, game: Game):
    pos = p.upperPosition
    return Pipe((pos[0] - game.camera_rect[0], pos[1]), p.upperSize, False)

def getLowerPipe(p, game: Game):
    pos = p.lowerPosition
    return Pipe((pos[0] - game.camera_rect[0], pos[1]), p.lowerSize, True)

while True:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.click()

    game.update()
    bird.update(game)
    background.update(game)
    scoreboard.update(game)
    pipes = [getUpperPipe(p, game) for p in game.pipes] + [getLowerPipe(p, game) for p in game.pipes]

    screen.fill(BACKGROUND_COLOR)
    for p in pipes:
        screen.blit(p.image, p.position)
    background.draw(screen)
    screen.blit(bird.image, bird.position)
    screen.blit(scoreboard.image, scoreboard.position)

    if game.dead:
        if failed == None:
            failed = FailedScreen(WINDOW_SIZE, game.score, game.best_score)
        screen.blit(failed.image, failed.position)
    else:
        failed = None

    pygame.display.flip()

pygame.quit()