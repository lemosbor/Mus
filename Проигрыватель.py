import pygame
#import playsound
#playsound.playsound('01.mp3', True)
from pygame import mixer  # Load the popular external library

mixer.init()
mixer.music.load('01.mp3')
mixer.music.play()
 
FPS = 60
W = 700  # ширина экрана
H = 300  # высота экрана
WHITE = (255, 255, 255)
BLUE = (0, 70, 225)
 
pygame.init()
sc = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
 
# координаты и радиус круга
x = W // 2
y = H // 2
r = 50
 
while 1:
    sc.fill(WHITE)
 
    pygame.draw.circle(sc, BLUE, (x, y), r)
 
    pygame.display.update()
 
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_LEFT:
                x -= 3
                mixer.music.play()
            elif i.key == pygame.K_RIGHT:
                x += 3
                mixer.music.stop()
 
    clock.tick(FPS)