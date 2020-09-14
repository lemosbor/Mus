import pygame # модуль для игр
#import playsound
#playsound.playsound('01.mp3', True)
from pygame import mixer  # библиотека для работы с музыкой
from pathlib import Path # библиотека для работы с папками
import os

WHITE = (255, 255, 255) # задаем цвет
pygame.init()
sc = pygame.display.set_mode((700, 300)) # создаем окошко 700 на 300 #x = W // 2 # координаты и радиус круга BLUE = (0, 70, 225) #y = H // 2 #r = 50
clock = pygame.time.Clock()
while 1: # создаем цикл
	sc.fill(WHITE) # заливаем окошко белым		
	#pygame.draw.circle(sc, BLUE, (x, y), r) 
	#pygame.display.update() #обновить экран ДЛЯ ГРАФИКИ
	#for i in pygame.event.get():
	for папка in Path('/Users/Илья/Music/Приёмка').iterdir(): #для всех подпапок в папке «Приёмка»
		for n in Path(папка).glob('*.mp3'): # в каждом файле с расширением mp3 рассматриваемой папки
			print(n)
			mixer.init()
			mixer.music.load(n) # загружаем файл
			mixer.music.play() # запускаем файл
			if i.type == pygame.QUIT: # если нажать ВЫХ
				exit() # то выйти
			elif i.type == pygame.KEYDOWN: #если нажать
				if i.key == pygame.K_LEFT: # влево
					mixer.music.stop()
					#os.remove(n) # удалить песню
				elif i.key == pygame.K_RIGHT: #вправо
					mixer.music.stop() 
		clock.tick(60) # обновление экрана с частотой 60 к/с
