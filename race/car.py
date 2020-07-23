import os
import pygame

from math import sin, radians, degrees
from pygame.math import Vector2


PPU = 32


class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "mini_car.png")

        self.car_image = pygame.image.load(image_path)
        self.position = Vector2(x / PPU, y / PPU)
        self.real_position = Vector2(x, y)

        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20

        self.acceleration = 0.0
        self.steering = 0.0
        self.free_deceleration = 2.0
        self.break_deceleration = 7.0

        self.rotated = None
        self.center_position = Vector2(0.0, 0.0)

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

        # Make car rect
        self.rotated = pygame.transform.rotate(self.car_image, self.angle)
        rotated_rect = self.rotated.get_rect()

        # Calculate position
        self.real_position = self.position * PPU
        self.center_position = (
            self.real_position.x + rotated_rect.width / 2, self.real_position.y + rotated_rect.height / 2)
