import os
import pygame
import random
import math

from pygame import Vector2

from race import car

# Color
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 180)
RED = (255, 0, 0)

# Action State
RUN = 3
EXIT = 4

# Track
GUIDE_WIDHT = 1

# Car
START_POINT = (30, 330)
MAX_BEAM_LEN = 150
BEAM_SURFACE = (150, 150)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.join(CURRENT_DIR, "../resources")


class Game:
    def __init__(self, ticks=60, auto=True):
        pygame.init()
        pygame.display.set_caption("Car tutorial")

        map_path = os.path.join(RESOURCE_DIR, "map.png")
        self.map_surface = pygame.image.load(map_path)
        self.map_mask = pygame.mask.from_surface(self.map_surface)

        mask_fx = pygame.mask.from_surface(
            pygame.transform.flip(self.map_surface, True, False))
        mask_fy = pygame.mask.from_surface(
            pygame.transform.flip(self.map_surface, False, True))
        mask_fx_fy = pygame.mask.from_surface(
            pygame.transform.flip(self.map_surface, True, True))
        self.flipped_masks = [[self.map_mask, mask_fy], [mask_fx, mask_fx_fy]]

        self.width = self.map_surface.get_width()
        self.height = self.map_surface.get_height()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.auto = auto
        self.action_status = RUN
        self.car = car.Car(*START_POINT)
        self.dt = 0
        self.ticks = ticks
        self.clock = pygame.time.Clock()
        self.beam_surface = pygame.Surface(BEAM_SURFACE, pygame.SRCALPHA)

    def run_car(self):
        while self.action_status is RUN:
            self.dt = self.clock.get_time() / 200

            # init screen
            self.init_screen()

            # Event queue
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                self.action_status = EXIT

            # Process moving
            self.process_moving_car()

            # Car update
            self.car.update(self.dt)

            # Car check position
            self.check_position_and_reset_position()

            # Calculate distance
            self.car.point_zero_angle = self.calculate_distance(
                self.car.center_position, self.car.angle)
            self.car.point_plus_45_angle = self.calculate_distance(
                self.car.center_position, self.car.angle + 45)
            self.car.point_minus_45_angle = self.calculate_distance(
                self.car.center_position, self.car.angle - 45)

            # Car check distance and reset position
            if self.car.center_position.distance_to(self.car.point_zero_angle) < 5:
                self.car.__init__(*START_POINT, angle=0)
            elif self.car.center_position.distance_to(self.car.point_minus_45_angle) < 5:
                self.car.__init__(*START_POINT, angle=0)
            elif self.car.center_position.distance_to(self.car.point_plus_45_angle) < 5:
                self.car.__init__(*START_POINT, angle=0)

            # Draw
            self.draw_screen()

            self.clock.tick(self.ticks)

        pygame.quit()

    def process_moving_car(self):
        if self.auto is True:
            # Car Acceleration
            self.car.acceleration = random.uniform(-self.car.max_acceleration / 4,
                                                  self.car.max_acceleration)
            # Car Steering
            # self.car.steering += random.randrange(-self.car.max_steering,
            #                                       self.car.max_steering) * self.dt
            minux_45_distance = self.car.center_position.distance_to(
                self.car.point_minus_45_angle)
            plus_45_distance = self.car.center_position.distance_to(
                self.car.point_plus_45_angle)

            if minux_45_distance < plus_45_distance:
                self.car.steering += self.car.max_steering * self.dt
            elif minux_45_distance > plus_45_distance:
                self.car.steering += -self.car.max_steering * self.dt
            else:
                self.car.steering = 0

        else:
            # User input
            pressed = pygame.key.get_pressed()

            # Car Acceleration
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
                    self.car.acceleration = - \
                        math.copysign(self.car.break_deceleration,
                                      self.car.velocity.x)
                else:
                    self.car.acceleration = -self.car.velocity.x / self.dt
            else:
                if abs(self.car.velocity.x) > self.dt * self.car.free_deceleration:
                    self.car.acceleration = - \
                        math.copysign(self.car.free_deceleration,
                                      self.car.velocity.x)
                else:
                    if self.dt != 0:
                        self.car.acceleration = -self.car.velocity.x / self.dt

            # Car Steering
            if pressed[pygame.K_RIGHT]:
                self.car.steering -= 30 * self.dt
            elif pressed[pygame.K_LEFT]:
                self.car.steering += 30 * self.dt
            else:
                self.car.steering = 0

        self.car.acceleration = max(-self.car.max_acceleration,
                                    min(self.car.acceleration, self.car.max_acceleration))
        self.car.steering = max(-self.car.max_steering,
                                min(self.car.steering, self.car.max_steering))

    def check_position_and_reset_position(self):
        if self.car.real_position.x > self.width:
            # car.position.x = 0.0
            self.car.__init__(*START_POINT, angle=0)

        elif self.car.position.x < 0.0:
            # car.position.x = float(self.width / ppu)
            self.car.__init__(*START_POINT, angle=0)

        if self.car.real_position.y > self.height:
            # car.position.y = 0.0
            self.car.__init__(*START_POINT, angle=0)

        elif self.car.position.y < 0.0:
            # car.position.y = float(self.height / ppu)
            self.car.__init__(*START_POINT, angle=0)

    def init_screen(self):
        self.screen.fill(BLACK)

    def draw_screen(self):
        # Draw track
        self.screen.blit(self.map_surface, self.map_surface.get_rect())

        # Draw car
        self.screen.blit(self.car.rotated, self.car.real_position)

        # Draw text
        self.printText(f'Generation : { 0 }', (10, 10))
        self.printText(f'Car velocity : {self.car.velocity}', (10, 30))
        self.printText(f'Car acceleration : {self.car.acceleration}', (10, 50))
        self.printText(f'Car steering : {self.car.steering}', (10, 70))
        # self.printText(f'Car steering : {self.car.steering}', 10, 90)

        pygame.display.update()

    def calculate_distance(self, start_position, angle) -> tuple:
        hit_position = None

        c = math.cos(math.radians(-angle))
        s = math.sin(math.radians(-angle))

        flip_x = c < 0
        flip_y = s < 0
        filpped_mask = self.flipped_masks[flip_x][flip_y]

        x_dest = self.beam_surface.get_width() * abs(c)
        y_dest = self.beam_surface.get_height() * abs(s)

        self.beam_surface.fill((0, 0, 0, 0))

        # draw a single beam to the beam surface based on computed final point
        pygame.draw.line(self.beam_surface, BLUE, (0, 0), (x_dest, y_dest))
        beam_mask = pygame.mask.from_surface(self.beam_surface)

        # find overlap between "global mask" and current beam mask
        offset_x = self.width - start_position.x if flip_x else start_position.x
        offset_y = self.height - start_position.y if flip_y else start_position.y

        hit = filpped_mask.overlap(
            beam_mask, (round(offset_x), round(offset_y)))
        if hit is not None and (hit[0] != start_position.x or hit[1] != start_position.y):
            hit_position = (
                self.width - hit[0] if flip_x else hit[0], self.height - hit[1] if flip_y else hit[1])
        else:
            hit_position = (start_position.x + MAX_BEAM_LEN * c,
                            start_position.y + MAX_BEAM_LEN * s)

        pygame.draw.circle(self.screen, RED, hit_position, 5)
        return hit_position

    def printText(self, text, position, font_size=15):
        # font loading, text size: 15
        font_path = os.path.join(RESOURCE_DIR, "NanumSquareOTF_acB.otf")
        fontObj = pygame.font.Font(font_path, font_size)
        printTextObj = fontObj.render(text, True, WHITE)
        printTextRect = printTextObj.get_rect()
        printTextRect.topleft = position
        self.screen.blit(printTextObj, printTextRect)
