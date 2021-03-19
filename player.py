from projectile import Projectile
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.health = 1000
        self.maxHealth = 1000
        self.attack = 50
        self.velocity = 8
        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 600
        self.all_projectiles = pygame.sprite.Group()
        self.game = game
        # Initialise jump
        self.jump_count = 5
        self.is_jump = False
        # Animation
        self.animation = [pygame.image.load(f'assets/player/player{i}.png') for i in range(1, 25)]  # list of all...
        # images for the attack animation
        self.animation_attack_count = 0
        self.is_attack = False

    # instantiation of the projectile class
    def projectile_attack(self):
        self.all_projectiles.add(Projectile(self))

    def move_right(self):
        if not self.game.check_collision(self.game.player, self.game.all_monsters):
            self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def jump(self):
        if not self.game.check_collision(self.game.player, self.game.all_meteors):
            neg = 1
            if self.jump_count >= -5:
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= int(self.jump_count ** 2) * neg
                self.jump_count -= 0.25
            else:
                self.rect.y = 600
                self.jump_count = 5
                self.is_jump = False

    def check_health(self, monster=True):
        if monster:
            for monster in self.game.all_monsters:
                if self.health > 0:
                    self.health -= monster.attack
                elif self.health <= 0:
                    self.game.all_monsters.remove(monster)
                    self.game.stop_game = True
        else:
            for meteor in self.game.all_meteors:
                if self.health > 0:
                    self.health -= meteor.damage
                elif self.health <= 0:
                    self.game.all_monsters.remove(meteor)
                    self.game.stop_game = True
