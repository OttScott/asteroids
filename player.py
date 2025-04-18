import sys
import random
import pygame
from constants import *
from circleshape import CircleShape
from bullet import Bullet

# Player class
class Player(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_timeout = 0.0
        self.bullet_list = []

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        # draw the triangle
        pygame.draw.polygon(screen, "white", self.triangle())

    def move(self, dt):
        # move the player
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += self.velocity * dt

        # wrap around the screen
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH

        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0: 
            self.position.y = SCREEN_HEIGHT
    
    def rotate(self, dt):
        # rotate the player
        self.rotation += PLAYER_TURN_SPEED * dt
        self.rotation %= 360

    def warp(self, asteroid_group=None):
        safe = False
        while not safe:
            # warp the player
            self.position.x = random.randint(0, SCREEN_WIDTH)
            self.position.y = random.randint(0, SCREEN_HEIGHT)
            self.rotation = random.randint(0, 360)
            safe = True
            
            # check if the player is in a safe zone (if we have an asteroid group)
            if asteroid_group:
                for asteroid in asteroid_group:
                    if self.is_colliding(asteroid):
                        safe = False
                        break
        

    def shoot(self):
        # shoot a bullet
        if self.shot_timeout > 0:
            return
        else:
            velocity = pygame.Vector2(0, 1).rotate(self.rotation) * BULLET_SPEED
            bullet = Bullet(self.position.x, self.position.y, BULLET_RADIUS, velocity)
            self.bullet_list.append(bullet)
            self.shot_timeout = BULLET_COOLDOWN
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity += pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_ACCEL * dt
            if self.velocity.length() > PLAYER_MAX_SPEED:
                self.velocity.scale_to_length(PLAYER_MAX_SPEED)
        if keys[pygame.K_s]:
            # The asteroid_group will be passed when we set it
            self.warp(getattr(self, 'asteroid_group', None))
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_ESCAPE] or (keys[pygame.K_c] and keys[pygame.K_LCTRL]):
            pygame.quit()
            sys.exit()

        self.position += self.velocity * dt

        # update the shot timeout
        if self.shot_timeout > 0:
            self.shot_timeout -= dt
        if self.shot_timeout < 0:
            self.shot_timeout = 0.0