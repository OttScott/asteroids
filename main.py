# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
import sys
from circleshape import *
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from bullet import Bullet

# *****************************************************************************
#                                     Main
# *****************************************************************************
def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    game_clock = pygame.time.Clock()
    dt = 0

    # initialize the game
    player_start_x = SCREEN_WIDTH / 2
    player_start_y = SCREEN_HEIGHT / 2

    grp_updatable = pygame.sprite.Group()
    grp_drawable = pygame.sprite.Group()

    Player.containers = (grp_updatable, grp_drawable)

    grp_bullets = pygame.sprite.Group()
    Bullet.containers = (grp_bullets, grp_updatable, grp_drawable)

    grp_asteroids = pygame.sprite.Group()
    Asteroid.containers = (grp_asteroids, grp_updatable, grp_drawable)
    AsteroidField.containers = (grp_updatable)

    # create the asteroid field
    asteroid_field = AsteroidField()

    player = Player(player_start_x, player_start_y, PLAYER_RADIUS)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while (True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")

        grp_updatable.update(dt)
        for obj in grp_drawable:
            obj.draw(screen)

        # check for collisions
        for asteroid in grp_asteroids:
            if player.is_colliding(asteroid):
                print("Game Over!")
                pygame.quit()
                sys.exit()
                
        for bullet in grp_bullets:
            for asteroid in grp_asteroids:
                if bullet.is_colliding(asteroid):
                    bullet.kill()
                    asteroid.split()
                    break

        pygame.display.flip()

        # update the game clock - End of the game loop
        dt = (game_clock.tick(60) / 1000)

if __name__ == "__main__":
    main()