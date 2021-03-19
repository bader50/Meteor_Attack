import pygame


class Projectile(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.velocity = 12
        self.image = pygame.image.load("assets/projectile.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 120
        self.rect.y = player.rect.y + 80
        self.player = player
        self.origin_image = self.image
        self.angle = 0

    def rotate(self):
        # rotation speed
        self.angle += 10
        # rotate the image, scale is the size of the image
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        # Center the rect of the image for the rotation
        self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move(self):
        self.rect.x += self.velocity
        self.rotate()

        # if the projectile touch the monster remove it
        if self.rect.x <= 1024:
            if self.player.game.check_collision(self, self.player.game.all_monsters):
                self.player.game.check_monster_health()
                self.remove()

        # Delete the different projectile out of screen
        if self.rect.x > 1080:
            self.remove()
