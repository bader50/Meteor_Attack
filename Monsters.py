import pygame
import random


class Monsters(pygame.sprite.Sprite):

    def __init__(self, game, kind):
        super().__init__()
        self.health = 100
        self.maxHealth = 100
        self.attack = 1
        self.velocity = random.randint(2, 10)
        self.kind = kind
        if kind == 1:
            self.image = pygame.image.load("assets/mummy.png")
            self.mummy_walking = [pygame.image.load(f'assets/mummy/mummy{i}.png') for i in range(1, 25)]
        elif kind == 2:
            self.image = pygame.image.load("assets/alien.png")
            self.image = pygame.transform.scale(self.image, (134, 134))
            self.alien_walking = [pygame.transform.scale(pygame.image.load(f'assets/alien/alien{i}.png'), (134, 134))
                                  for i in range(1, 25)]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(900, game.round * 1000)
        self.rect.y = 641
        self.game = game
        # Animation
        self.is_moving = True
        self.walking_count = 0

    def move(self):
        # Check collision between the current monster and the player
        if self.rect.x <= 1024:
            if not self.game.check_collision(self, self.game.all_player):
                self.is_moving = True
                self.rect.x -= self.velocity
            else:
                self.is_moving = False
                self.game.player.check_health()
        else:
            self.is_moving = True
            self.rect.x -= self.velocity

        # Check if the monster is out boundaries
        if self.rect.x < 0:
            self.remove()

    def remove(self):
        self.game.all_monsters.remove(self)
