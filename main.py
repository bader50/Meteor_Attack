import sys
import yappi
from game import Game
import pygame

yappi.set_clock_type("cpu") # Use set_clock_type("wall") for wall time
yappi.start()

pygame.init()

# set title of the window
pygame.display.set_caption("Meteor Attack")
# set size of the window
window = pygame.display.set_mode((1024, 900))
# Load the background image
background = pygame.image.load("assets/bg.jpg")

# game instantiation
game = Game()

Last_total_kill = 0

# font
font = pygame.font.SysFont('comicsans', 30)
# variable for the infinite loop
running = True
banner_running = True
game_running = False

while running:
    # Banner screen
    if banner_running:
        pygame.time.delay(100)
        # Draw the background on the created screen
        window.blit(background, (0, -100))

        # Banner
        banner = pygame.image.load('assets/banner.png')
        button = pygame.image.load('assets/button.png')

        banner = pygame.transform.scale(banner, (500, 500))
        button = pygame.transform.scale(button, (400, 150))

        window.blit(button, (window.get_width() // 2 - 190, window.get_height() // 2 + 10))
        window.blit(banner, (window.get_width() // 2 - 250, window.get_height() // 2 - 350))

        # Display Total last kill number
        if Last_total_kill != 0:
            text = font.render("You've killed " + str(Last_total_kill) + " monsters", 1000, (255, 255, 255))
            window.blit(text, (10, 10))

        # update the window
        pygame.display.flip()

        # Event Detection
        for event in pygame.event.get():
            # Closing game event
            if event.type == pygame.QUIT:
                pygame.quit()
                # sys.exit()

            # Mouse event
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                #get the location of the mouse click to start the game
                if window.get_width() // 2 - 190 < mx < (window.get_width() // 2 - 190 + 400):
                    if window.get_height() // 2 + 10 < my < (window.get_height() // 2 + 10 + 150):
                        banner_running = False
                        game_running = True
                        game.all_player.remove(game.player)
                        game = Game()

    # Game starting
    if game_running:

        game.clock = pygame.time.get_ticks() // 1000

        # Meteor attack
        if game.clock == game.meteor_time:

            for monster in game.all_monsters:
                monster.remove()
            game.is_meteor = True
            game.meteor_time += game.meteor_delay

        # Draw the background on the created screen
        window.blit(background, (0, -100))
        # Draw the player character
        # Attack animation
        if game.player.is_attack:
            if game.player.animation_attack_count + 1 >= 24:
                game.player.animation_attack_count = 0
                game.player.is_attack = False

            if game.player.is_attack:
                window.blit(game.player.animation[game.player.animation_attack_count], game.player.rect)
                game.player.animation_attack_count += 2
            else:
                window.blit(game.player.image, game.player.rect)
        else:
            window.blit(game.player.image, game.player.rect)

        # Player background Health Bar
        pygame.draw.rect(window,
                         (0, 0, 0),
                         (game.player.rect.x + 75,
                          game.player.rect.y - 10,
                          (game.player.maxHealth // 2) // 10,
                          5))

        # Player foreground Health Bar
        pygame.draw.rect(window,
                         (0, 255, 0),
                         (game.player.rect.x + 75,
                          game.player.rect.y - 10,
                          ((game.player.maxHealth - (game.player.maxHealth - game.player.health)) // 2) // 10,
                          5))

        # monster animation
        for monster in game.all_monsters:
            if monster.is_moving:
                # mummy
                if monster.kind == 1:
                    if monster.walking_count + 1 >= 24:
                        monster.walking_count = 0
                        monster.is_moving = False

                    if monster.is_moving:
                        window.blit(monster.mummy_walking[monster.walking_count], monster.rect)
                        monster.walking_count += 1
                    else:
                        window.blit(monster.image, monster.rect)
                # Alien
                if monster.kind == 2:
                    if monster.walking_count + 1 >= 24:
                        monster.walking_count = 0
                        monster.is_moving = False

                    if monster.is_moving:
                        window.blit(monster.alien_walking[monster.walking_count], monster.rect)
                        monster.walking_count += 1
                    else:
                        window.blit(monster.image, monster.rect)
            else:
                window.blit(monster.image, monster.rect)

        # draw each projectile
        game.player.all_projectiles.draw(window)

        # move each monster
        for monster in game.all_monsters:
            monster.move()
            # Health bar
            pygame.draw.rect(window, (0, 0, 0), (monster.rect.x + 40, monster.rect.y - 10, monster.maxHealth // 2, 5))
            pygame.draw.rect(window, (0, 255, 0), (
                monster.rect.x + 40, monster.rect.y - 10,
                (monster.maxHealth - (monster.maxHealth - monster.health)) // 2,
                5))

        # move each projectile
        for projectile in game.player.all_projectiles:
            projectile.move()

        # Jumping part
        if game.player.is_jump:
            game.player.jump()

        # verify if the key right is pushed, limit the sliding in the right side (take into account the rectangle of the
        # image width)
        if game.pressed.get(pygame.K_RIGHT) and game.player.rect.x + game.player.rect.width < window.get_width():
            game.player.move_right()
        # same for the left
        elif game.pressed.get(pygame.K_LEFT) and game.player.rect.x > 0:
            game.player.move_left()

        # display kill number
        text = font.render("kill: " + str(game.kill_number), 1, (0, 0, 0))
        window.blit(text, (10, 10))

        # update round
        game.manage_round()

        # move each meteor
        for meteor in game.all_meteors:
            meteor.move()

        # Respawn management
        if game.is_meteor:
            game.generate_meteors()
        elif len(game.all_meteors) == 0:
            if game.respawn_count == 100:
                if len(game.all_monsters) < game.round:
                    game.respawn()
                game.respawn_count = 0
            else:
                game.respawn_count += 1

        # Draw each meteor
        game.all_meteors.draw(window)

        # Stop game
        if game.stop_game:
            Last_total_kill = game.kill_number
            game_running = False
            banner_running = True

        # update the window
        pygame.display.flip()

        # Event Detection
        for event in pygame.event.get():
            # Closing game event
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                # sys.exit()
            # key pushed
            elif event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True
                # SPACE for attack
                if event.key == pygame.K_SPACE:
                    game.player.projectile_attack()
                    game.player.is_attack = True
                # UP for jumping
                elif event.key == pygame.K_UP:
                    game.player.is_jump = True
            # key unpushed
            elif event.type == pygame.KEYUP:
                game.pressed[event.key] = False
yappi.stop()
yappi.get_func_stats().print_all()
yappi.get_thread_stats().print_all()
