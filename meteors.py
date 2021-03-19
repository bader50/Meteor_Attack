import pygame
import random


class Meteors(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.velocity = 5
        self.damage = 20
        self.image = pygame.image.load('assets/comet.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(10, 1000)
        self.rect.y = random.randint(-500, 0)
        self.game = game

    def move(self):
        # Check collision between the current comet and the player
        if self.rect.y >= 600:
            if not self.game.check_collision(self, self.game.all_player):
                self.rect.y += self.velocity
            else:
                self.game.player.check_health(monster=False)
                self.game.all_meteors.remove(self)
        else:
            self.rect.y += self.velocity

        if self.rect.y >= 900:
            self.game.all_meteors.remove(self)
