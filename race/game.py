import os
import pygame
import random

from race import car as c
from math import sin, radians, degrees, copysign

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 180)
RED = (255, 0, 0)


class Game:

    def __init__(self, width, height, ticks=60, auto=True):
        pygame.init()
        pygame.display.set_caption("Car tutorial")

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.ticks = ticks
        self.auto = auto
        self.exit = False
        self.car = c.Car(self.width / 2, self.height / 2)
        self.dt = 0

    def run(self):
        while not self.exit:
            self.dt = self.clock.get_time() / 200

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # Process moving
            self.process_moving_car()

            # Car check position
            self.check_and_reset_position()

            # Car update
            self.car.update(self.dt)

            # Draw
            self.draw_screen()

            self.clock.tick(self.ticks)

        pygame.quit()

    def process_moving_car(self):
        # Car Acceleration
        if self.auto is True:
            self.car.acceleration = random.randrange(int(-self.car.max_acceleration / 2),
                                                     self.car.max_acceleration)

        else:
            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                if self.car.velocity.x < 0:
                    self.car.acceleration = self.car.break_deceleration
                else:
                    self.car.acceleration += 1 * self.dt
            elif pressed[pygame.K_DOWN]:
                if self.car.velocity.x > 0:
                    self.car.acceleration = -self.car.break_deceleration
                else:
                    self.car.acceleration -= 1 * self.dt
            elif pressed[pygame.K_SPACE]:
                if abs(self.car.velocity.x) > self.dt * self.car.break_deceleration:
                    self.car.acceleration = -copysign(self.car.break_deceleration, self.car.velocity.x)
                else:
                    self.car.acceleration = -self.car.velocity.x / self.dt
            else:
                if abs(self.car.velocity.x) > self.dt * self.car.free_deceleration:
                    self.car.acceleration = -copysign(self.car.free_deceleration, self.car.velocity.x)
                else:
                    if self.dt != 0:
                        self.car.acceleration = -self.car.velocity.x / self.dt

        self.car.acceleration = max(-self.car.max_acceleration,
                                    min(self.car.acceleration, self.car.max_acceleration))
        print(f'car.accel: {self.car.acceleration}')

        # Car Steering
        if self.auto is True:
            self.car.steering += random.randrange(-self.car.max_steering, self.car.max_steering) * self.dt

        else:
            if pressed[pygame.K_RIGHT]:
                self.car.steering -= 30 * self.dt
            elif pressed[pygame.K_LEFT]:
                self.car.steering += 30 * self.dt
            else:
                self.car.steering = 0

        self.car.steering = max(-self.car.max_steering, min(self.car.steering, self.car.max_steering))
        print(f'car.steering: {self.car.steering}')

    def check_and_reset_position(self):
        if self.car.real_position.x > self.width:
            # car.position.x = 0.0
            self.car.__init__(self.width / 2, self.height / 2, angle=random.randrange(0, 360))
        elif self.car.position.x < 0.0:
            # car.position.x = float(self.width / ppu)
            self.car.__init__(self.width / 2, self.height / 2, angle=random.randrange(0, 360))

        if self.car.real_position.y > self.height:
            # car.position.y = 0.0
            self.car.__init__(self.width / 2, self.height / 2, angle=random.randrange(0, 360))
        elif self.car.position.y < 0.0:
            # car.position.y = float(self.height / ppu)
            self.car.__init__(self.width / 2, self.height / 2, angle=random.randrange(0, 360))

    def draw_screen(self):
        # Draw background
        self.screen.fill(BLACK)

        # Draw car
        self.screen.blit(self.car.rotated, self.car.real_position)

        # Draw middle circle
        print(f'position: {self.car.center_position}')
        pygame.draw.circle(self.screen, RED, self.car.center_position, 4, 0)

        pygame.display.flip()
