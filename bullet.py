from circleshape import CircleShape
from constants import *
import pygame

class Bullet(CircleShape):
    def __init__(self, x, y, radius, vec2d_velocity):
        super().__init__(x, y, radius)
        self.outline = "yellow"
        self.TimeOut = BULLET_LIFETIME
        self.setVelocity(vec2d_velocity)
        
    def update(self, dt):
        # Update the position of the bullet
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
        
        # Decrease the lifetime of the bullet
        self.TimeOut -= dt
        if self.TimeOut <= 0:
            self.kill()  # Remove the bullet if its lifetime is over

    def draw(self, screen):
        # Draw the bullet as a circle
        pygame.draw.circle(screen, self.outline, (int(self.position.x), int(self.position.y)), self.radius)

    def setVelocity(self, vec2d_velocity):
        # Set the velocity of the bullet
        self.velocity = vec2d_velocity
        self.velocity.scale_to_length(BULLET_SPEED)

