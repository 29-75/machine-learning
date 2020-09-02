import math
import os
import pygame
import random
import time
from math import sin, radians, degrees, copysign
from pygame.math import Vector2

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255,255,255)
start_x=3
start_y=11
width=1024
height=768

current_dir = os.path.dirname(os.path.abspath(__file__))
car_image_path = os.path.join(current_dir, "res/wolf2.png")
track_image_path = os.path.join(current_dir, "res/jhjtrack.png")
car_image = pygame.image.load(car_image_path)
track_image = pygame.image.load(track_image_path)
mask = pygame.mask.from_surface(track_image)
mask_fx = pygame.mask.from_surface(pygame.transform.flip(track_image, True, False))
mask_fy = pygame.mask.from_surface(pygame.transform.flip(track_image, False, True))
mask_fx_fy = pygame.mask.from_surface(pygame.transform.flip(track_image, True, True))
flipped_masks = [[mask, mask_fy], [mask_fx, mask_fx_fy]]
beam_surface = pygame.Surface((width, height), pygame.SRCALPHA)

car_mask = pygame.mask.from_surface(car_image)
track_mask = pygame.mask.from_surface(track_image)

car_size = car_image.get_size()
class Car:
    def __init__(self, angle, length=4, max_steering=30, max_acceleration=5.0):
        self.position = Vector2(start_x, start_y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20
        self.brake_deceleration = 10
        self.free_deceleration = 2

        self.acceleration = 0.0
        self.steering = 0.0
    def __copy__(self):
        new_mask = super().__copy__()
        return new_mask
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
    
    def reset(self, angle):
        self.position = Vector2(start_x, start_y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.acceleration = 0.0
        self.steering = 0.0       


class Game():
    def __init__(self):
        pygame.init()
        # https://velog.io/@korca0220/Pygame-2D%EA%B2%8C%EC%9E%84-%EB%A7%8C%EB%93%A4%EA%B8%B0-Sprites
        # game -> mygame 입력중...
        # groups 으로 묶어서 add로 충돌감지 할듯. .?
        
        pygame.display.set_caption("자ㅋ동ㅋ차ㅋ 게임")
        self.width = 1024
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.ticks = 30
        self.exit = False
        self.mousepos1=[]
        self.mousepos2=[]

    def drawmap(self):
        clock = pygame.time.Clock()

        mousedown = False
        #mousepos1 = []
        #mousepos2 = []
        nextTrack = False
        endFlag = 0
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousedown = True
            elif event.type == pygame.MOUSEBUTTONUP:
                endFlag += 1
                mousedown = False
                nextTrack = True
        #        mousepos.clear()
            elif event.type == pygame.MOUSEMOTION:
                if mousedown:
                    if nextTrack == False:
                        self.mousepos1.append(event.pos)
                    else: self.mousepos2.append(event.pos)

            self.screen.fill((0, 0, 0))

            if len(self.mousepos1) > 1:
                pygame.draw.lines(self.screen, RED, False, self.mousepos1)
            if len(self.mousepos2) > 1:
                pygame.draw.lines(self.screen, GREEN, False, self.mousepos2)

            pygame.display.update()
            clock.tick(30)

            # 2번째 트랙 그리면 while 문 종료
            if nextTrack == True and endFlag == 2 :
                break;

        # while문 빠져나와서 그림 저장하고 pygame 종료
        #pygame.image.save(self.screen, "test.jpg")

    def run(self):
        car = Car(0)
        ppu = 32

        # 장애물
        #asset_path = os.path.join(current_dir, "car.png")
        #asset_image = pygame.image.load(asset_path)

        breaker = False      
        while not self.exit:

            dt = self.clock.get_time() / 500

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # auto input   
            """    
            car.acceleration = max(-car.max_acceleration, min(random.randint(-2, 5), car.max_acceleration))

            choiced2 = random.randint(0,1)
            if choiced2 == 0:
                car.steering -= 30 * dt
            elif choiced2 == 1:
                car.steering += 30 * dt
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))
            """
            # original input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                if car.velocity.x < 0:
                    car.acceleration = car.brake_deceleration
                else:
                    car.acceleration += 1 * dt
            elif pressed[pygame.K_DOWN]:
                if car.velocity.x > 0:
                    car.acceleration = -car.brake_deceleration
                else:
                    car.acceleration -= 1 * dt
            elif pressed[pygame.K_SPACE]:
                if abs(car.velocity.x) > dt * car.brake_deceleration:
                    car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
                else:
                    car.acceleration = -car.velocity.x / dt
            else:
                if abs(car.velocity.x) > dt * car.free_deceleration:
                    car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
                else:
                    if dt != 0:
                        car.acceleration = -car.velocity.x / dt
            car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

            if pressed[pygame.K_RIGHT]:
                car.steering -= 30 * dt
            elif pressed[pygame.K_LEFT]:
                car.steering += 30 * dt
            else:
                car.steering = 0
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))




            # 뱀 코드 참고해서 generate 시켜서 데이터 축적하고 model 만드는거 추가해야함.

            # Logic
            car.update(dt)

            # collide with 모퉁이
            if car.position[0] < 0 or car.position[1] < 0 or car.position[0] * ppu > self.width or car.position[1] * ppu > self.height :
                car.reset(0)

            # Drawing
            self.screen.fill((255, 255, 255))
            self.screen.blit(track_image, (0,0))
            # pygame.draw.lines(self.screen, GREEN, False, self.mousepos1)
            # pygame.draw.lines(self.screen, RED, False, self.mousepos2)
            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()
            car_pos = car.position * ppu - (rect.width / 2, rect.height / 2)

            # for angle in range(0, 359, 30):
            for angle in range(0, 359, 45):
                self.draw_beam(angle, car_pos + (rect.width / 2, rect.height / 2))

            self.screen.blit(rotated, car_pos)
            
            if self.crash(rotated, car_pos):
                breaker = True


            # mask overlap 충돌 코드
            # surface는 rect 기반으로 line은 안되지않을까?
            """
            mouse1_mask = pygame.Mask.from_surface(self.mousepos1)
            mouse2_mask = pygame.Mask.from_surface(self.mousepos2)
            car_mask = car.__copy__()
            print(car_mask.overlap_area(mouse1_mask, 1))
            print(car_mask.overlap_area(mouse2_mask, 1))
            """
            # rect 충돌 코드
            """
            c = pygame.Rect(car.position.x*ppu,car.position.y*ppu,10,10)
            for i in range(len(self.mousepos1)):
                a = pygame.Rect(self.mousepos1[i][0],self.mousepos1[i][1],2,2)
                pygame.draw.rect(self.screen, (0, 255, 0), a)

                if a.colliderect(c) :
                    print("colliderect")
                    breaker = True
                    break
            for i in range(len(self.mousepos2)):
                b = pygame.Rect(self.mousepos2[i][0],self.mousepos2[i][1],2,2)

                pygame.draw.rect(self.screen, (0, 255, 0), b)

                if b.colliderect(c) :
                    print("colliderect")
                    breaker = True
                    break
            if breaker == True : 
                car.reset(10,10,random.randint(0,360))
                breaker = False
                #break
            """

            # font 
            fontObj = pygame.font.Font('HoonWhitecatR.ttf', 20)    
            # print position
            carPositionText = "car position: " + str(car.position)
            carPositionTextObj = fontObj.render(carPositionText, True, WHITE) 
            carPositionRect = carPositionTextObj.get_rect();              
            carPositionRect.topleft = (3, 3)                              
            self.screen.blit(carPositionTextObj, carPositionRect)
            # print steering
            carSteeringText = "car steering: " + str(car.steering)
            carSteeringTextObj = fontObj.render(carSteeringText, True, WHITE)
            carSteeringRect = carSteeringTextObj.get_rect();                
            carSteeringRect.topleft = (3, 20)                               
            self.screen.blit(carSteeringTextObj, carSteeringRect)
            # print accelaration
            carAccelerationText = "car acceleration: " + str(car.acceleration)
            carAccelerationTextObj = fontObj.render(carAccelerationText, True, WHITE)  
            carAccelerationRect = carAccelerationTextObj.get_rect();                    
            carAccelerationRect.topleft = (3, 37)                             
            self.screen.blit(carAccelerationTextObj, carAccelerationRect)
            # print velocity
            carVelocityText = "car velocity: " + str(car.velocity[0])
            carVelocityTextObj = fontObj.render(carVelocityText, True, WHITE) 
            carVelocityRect = carVelocityTextObj.get_rect();                     
            carVelocityRect.topleft = (3, 54)                                    
            self.screen.blit(carVelocityTextObj, carVelocityRect)
            
            pygame.display.flip()
            self.clock.tick(self.ticks)
            if breaker:
                breaker = False
                car.reset(0)
        pygame.quit()

    def draw_beam(self, angle, pos):
        c = math.cos(math.radians(angle))
        s = math.sin(math.radians(angle))

        flip_x = c < 0
        flip_y = s < 0
        filpped_mask = flipped_masks[flip_x][flip_y]

        # compute beam final point
        x_dest = width * abs(c)
        y_dest = height * abs(s)

        beam_surface.fill((0, 0, 0, 0))

        # draw a single beam to the beam surface based on computed final point
        pygame.draw.line(beam_surface, BLUE, (0, 0), (x_dest, y_dest))
        beam_mask = pygame.mask.from_surface(beam_surface)

        # find overlap between "global mask" and current beam mask
        offset_x = width-1-pos[0] if flip_x else pos[0]
        offset_y = height-1-pos[1] if flip_y else pos[1]
        
        hit = filpped_mask.overlap(beam_mask, (int(offset_x), int(offset_y)))
        
        if hit is not None and (hit[0] != pos[0] or hit[1] != pos[1]):
            hx = width-1 - hit[0] if flip_x else hit[0]
            hy = height-1 - hit[1] if flip_y else hit[1]
            hit_pos = (hx, hy)

            pygame.draw.line(self.screen, BLUE, pos, hit_pos)
            pygame.draw.circle(self.screen, GREEN, hit_pos, 3)

    def crash(self, rotated, car_pos):
        iscrash = track_mask.overlap(car_mask, (int(car_pos.x), int(car_pos.y)))
        if iscrash:
            print(iscrash)
            fontObj = pygame.font.Font('HoonWhitecatR.ttf', 30)
            carCrashText = " c r a s h ! ( {0[0]} , {0[1]} )".format(iscrash)
            carCrashTextObj = fontObj.render(carCrashText, True, RED)
            carCrashRect = carCrashTextObj.get_rect();                
            carCrashRect.topleft = (100, 100)                               
            self.screen.blit(carCrashTextObj, carCrashRect)
            rotatedRect = self.screen.blit(rotated, car_pos)
            pygame.draw.rect(self.screen, RED, rotatedRect, 2)
            return True
        else:
            return False



if __name__ == '__main__':
    game = Game()
    # game.drawmap()
    game.run()