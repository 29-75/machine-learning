import math
import os
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
        self.position = Vector2(x, y)
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
    
    def reset(self, x, y):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = 0
        self.acceleration = 0.0
        self.steering = 0.0       


class Game():
    def __init__(self):
        pygame.init()
        # https://velog.io/@korca0220/Pygame-2D%EA%B2%8C%EC%9E%84-%EB%A7%8C%EB%93%A4%EA%B8%B0-Sprites
        # game -> mygame 입력중...
        # groups 으로 묶어서 add로 충돌감지 할듯. .?
        
        pygame.display.set_caption("자ㅋ동ㅋ차ㅋ 게임")
        self.width = 1280
        self.height = 700
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
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "wolf2.png")
        car_image = pygame.image.load(image_path)
        car = Car(10, 10)
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

            # User input
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

            # Logic
            car.update(dt)

            # collide with 모퉁이
            if car.position[0] < 0 or car.position[1] < 0 or car.position[0] * ppu > self.width or car.position[1] * ppu > self.height :
                car.reset(10,10)

            # Drawing
            self.screen.fill((0, 0, 0))
            pygame.draw.lines(self.screen, GREEN, False, self.mousepos1)
            pygame.draw.lines(self.screen, RED, False, self.mousepos2)
            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()
            self.screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))
            
            #################### 그림 mousepos 랑 car랑 충돌 하는거 감지해야됨
            # 자동차에서 나가는 직선 하나를 그리고, 선과 poly 의 접점을 구해서 그 접점까지의 거리로 판단한다.
            
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
                car.reset(10,10)
                breaker = False
                #break
            # font 
            WHITE = (255,255,255)
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
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.drawmap()
    game.run()