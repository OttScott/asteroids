import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
    def update(self, dt):
        # Update the position of the asteroid
        self.position += self.velocity * dt
        
        # Wrap around the screen
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH

        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = SCREEN_HEIGHT

    def draw(self, screen):
        # Draw the asteroid as a circle
        pygame.draw.circle(screen, "gray", (int(self.position.x), int(self.position.y)), self.radius)

    def split(self):
        self.kill()
        # Split the asteroid into smaller ones
        if (self.radius > ASTEROID_MIN_RADIUS):
            for i in range(2):
                new_radius = self.radius / 2
                new_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
                new_asteroid.velocity = (self.velocity.rotate(i * random.randint(-45, 45))) * random.uniform(0.4, 1.6)
                new_asteroid.add(self.containers)
        
