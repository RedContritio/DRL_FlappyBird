import pygame

from imgs.scoreboard import make_scoreboard

class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self, window_size, score):
        super().__init__()
        self.score = score
        self.window_size = window_size
        image = make_scoreboard(self.window_size, score, 0)
        self.image = pygame.image.frombuffer(image.tobytes(), image.shape[:2][::-1], 'RGBA')
        self.position = (0, 0)

    def update(self, game):
        if game.score != self.score:
            self.score = game.score
            image = make_scoreboard(self.window_size, self.score, game.best_score)
            self.image = pygame.image.frombuffer(image.tobytes(), image.shape[:2][::-1], 'RGBA')