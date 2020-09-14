import pygame # модуль для игр
#import playsound
#playsound.playsound('01.mp3', True)
from pygame import mixer  # библиотека для работы с музыкой
mixer.init()
mixer.music.load('01.mp3') # загружаем файл
mixer.music.play() # запускаем файл

FPS = 60 # частота обновления
W = 700  # ширина экрана
H = 300  # высота экрана
WHITE = (255, 255, 255) # задаем цвет
BLUE = (0, 70, 225)
pygame.init()
sc = pygame.display.set_mode((W, H)) # создаем окошко
clock = pygame.time.Clock()
#x = W // 2 # координаты и радиус круга
#y = H // 2
#r = 50
while 1: # создаем цикл
	sc.fill(WHITE) # заливаем окошко белым 
		for n in Path(папка).glob('*.mp3'):
		#pygame.draw.circle(sc, BLUE, (x, y), r) 
		#pygame.display.update() #обновить экран ДЛЯ ГРАФИКИ
		for i in pygame.event.get():
          if i.type == pygame.QUIT: # если нажать ВЫХ
              exit() # то выйти
          elif i.type == pygame.KEYDOWN: #если нажать
              if i.key == pygame.K_LEFT: # влево
                  mixer.music.play()
              elif i.key == pygame.K_RIGHT: #вправо
                  mixer.music.stop() 
      clock.tick(FPS) # обновление экрана
