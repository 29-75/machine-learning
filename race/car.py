import os
import pygame
import math

from math import sin, radians, degrees
from pygame.math import Vector2

PPU = 32
MAX_DISTANCE = 100
MAX_VELOCITY = 0.4
MAX_ACCELERATION = 0.1
MAX_STEERING = 40
FREE_DECELERATION = 2.0
BREAK_DECELERATION = 7.0
ZERO_XY = (0.0, 0.0)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.join(CURRENT_DIR, "../resources")

class Car:
    def __init__(self, x, y, angle=0.0, length=1):
        image_path = os.path.join(RESOURCE_DIR, "mini_car.png")
        self.car_image = pygame.image.load(image_path)
        self.position = Vector2(x / PPU, y / PPU)
        self.real_position = Vector2(x, y)

        self.angle = angle
        self.length = length
        self.max_acceleration = MAX_ACCELERATION
        self.max_steering = MAX_STEERING
        self.max_velocity = MAX_VELOCITY
        self.free_deceleration = FREE_DECELERATION
        self.break_deceleration = BREAK_DECELERATION
        self.velocity = Vector2(*ZERO_XY)
        self.acceleration = 0.0
        self.steering = 0.0

        self.rotated = pygame.transform.rotate(self.car_image, self.angle)
        self.center_position = Vector2(
            self.real_position.x + self.car_image.get_rect().width / 2,
            self.real_position.y + self.car_image.get_rect().height / 2)

        # line
        self.point_minus_45_angle = ZERO_XY
        self.point_zero_angle = ZERO_XY
        self.point_plus_45_angle = ZERO_XY

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity,
                              min(self.velocity.x, self.max_velocity))

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
        self.center_position.x = self.real_position.x + rotated_rect.width / 2
        self.center_position.y = self.real_position.y + rotated_rect.height / 2
