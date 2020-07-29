import pygame

pygame.init()
screen = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()

mousedown = False
mousepos1 = []
mousepos2 = []
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
                 mousepos1.append(event.pos)
            else: mousepos2.append(event.pos)

    screen.fill((0, 0, 0))

    if len(mousepos1) > 1:
        pygame.draw.lines(screen, (255, 0, 0), False, mousepos1)
    if len(mousepos2) > 1:
        pygame.draw.lines(screen, (0, 255, 0), False, mousepos2)

    pygame.display.update()
    clock.tick(30)

    # 2번째 트랙 그리면 while 문 종료
    if nextTrack == True and endFlag == 2 :
        break;


# while문 빠져나와서 그림 저장하고 pygame 종료
pygame.image.save(screen, "test.jpg")

pygame.quit()