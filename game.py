from player import Player
from Monsters import Monsters
from meteors import Meteors
import pygame


class Game:
    def __init__(self):
        self.player = Player(self)
        self.all_player = pygame.sprite.Group()
        self.all_player.add(self.player)
        # Meteors variables
        self.all_meteors = pygame.sprite.Group()
        self.is_meteor = False
        # number of meteor generated
        self.meteor_count = 0
        # Keys Dict
        self.pressed = {}
        self.all_monsters = pygame.sprite.Group()
        # round management
        self.clock = 0
        self.round = 1
        self.round_duration = 60  # second
        self.respawn()
        self.respawn_count = 0
        self.kill_number = 0
        self.round_kill_number = 0
        self.stop_game = False
        # time of each attack compared to the clock
        self.meteor_time = 60
        # delay between 2 meteor attack
        self.meteor_delay = 60

    def respawn(self):
        if self.round % 2 != 0:
            self.all_monsters.add(Monsters(self, 1))
        elif self.round % 2 == 0:
            self.all_monsters.add(Monsters(self, 2))

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def check_monster_health(self):
        for monster in self.all_monsters:
            if self.check_collision(monster, self.player.all_projectiles):
                if monster.health > 0:
                    monster.health -= self.player.attack
                elif monster.health <= 0:
                    self.kill_number += 1
                    self.round_kill_number += 1
                    monster.remove()

    def manage_round(self):
        if self.round_kill_number >= self.round:
            self.round += 1
            self.round_kill_number = 0

    def generate_meteors(self):
        if self.meteor_count <= 5:
            self.all_meteors.add(Meteors(self))
            self.meteor_count += 1
        else:
            self.is_meteor = False
            self.meteor_count = 0
