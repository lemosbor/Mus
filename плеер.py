import os
from io import BytesIO
from itertools import cycle # модуль циклов
import tkinter as tk # Python3
from tkinter import *
from tkinter import font as tkFont
import shutil # модуль удаления папки целиком
from pygame import mixer # модуль воспроизведения музыки
from pathlib import Path
песни = [] # создаем перечень проигрываемых треков

for n in Path('/Музыка/Приёмка').glob('*.mp3'): #создаем перечень треков в папке Приёмка
    песни.append(str(n)) #добавляем имя пути демо-трека
if len(песни) == 0: #если демо-треков нет
    способ = 2 # то прослушиваем по способу № 2
    print("Демо-треков в папке Приёмка нет. Переходим к прослушиванию песен в папках Зачистки")
    for папка in Path('/Музыка/Зачистка').iterdir(): #для всех подпапок в папке «Зачистка»
        if папка.is_dir() == True: # если папка
            for n in Path(папка).glob('*.mp3'): # если mp3 файл
                if Path(n).stat().st_size > 512000: #если файл размером более 500 кб
                    песни.append(str(n)) #добавляем имя пути файла-песни — её название
    print("Песен к прослушиванию:", len(песни))
else: # если демо-треки есть
    способ = 1 # то прослушиваем по способу № 1
    print("Прослушиваем демо-треки, в количестве", len(песни))

class App(tk.Tk): #'''Tk window/label adjusts to size of image'''
    def __init__(self, инфо): # the root will be self
        tk.Tk.__init__(self)# allows repeat cycling through the pictures # store as (img_object, img_name) tuple
        self.музыкацикл = cycle(ino for ino in песни)
        helv36 = tkFont.Font(family='Helvetica', size=36, weight=tkFont.BOLD)
        self.Кудалить = tk.Button(self, text = 'удалить', font=helv36) #https://habr.com/ru/post/133337/
        self.Коставить = tk.Button(self, text = 'оставить', font=helv36)
        self.Кперемотать = tk.Button(self, text = 'перемотать', font=helv36)
        self.Кудалить.bind("<Button-1>", self.ккласс0)
        self.Коставить.bind("<Button-1>", self.ккласс1)
        self.Кперемотать.bind("<Button-1>", self.перемотка)      
        self.Кудалить.pack(side = 'left')
        self.Коставить.pack(side = 'right')
        self.Кперемотать.pack(side = 'bottom')
    def перебор(self): # собственно перебор фоторафий
        self.музыка= next(self.музыкацикл) #отображаемая информация
        self.bind('<Left>', self.ккласс0) # если жмём кнопку Влево, то вызываем команду класс0
        self.bind('<Right>', self.ккласс1) # если жмём кнопку Вправо, то вызываем команду класс0
        self.bind('<space>', self.перемотка) # если жмём кнопку Пробел, то вызываем команду перемотка
        mixer.init()
        mixer.music.load(self.музыка) # загружаем файл
        mixer.music.play() # запускаем файл
        self.n=30
    def пуск(self): #запускаем панель
        self.mainloop()
    def ккласс1(self, event): # последовательность действий для команды класс1 — Оставить        
        mixer.music.load('/01.mp3') #предпроигрыш для освобождения трека
        if способ ==1: #если способ № 1
            папка = Path(self.музыка).stem #определяем название целевой папки по имени демо-трека
            Path("/Музыка/Приёмка/"+папка).replace("/Музыка/Зачистка/"+папка) #перемещаем папку в Зачистку
            Path(self.музыка).unlink() #удаляем демо-трек
        if способ ==2: #если способ № 2
            Path(self.музыка).replace("/Users/Илья/Music/"+Path(self.музыка).name) #перемещаем в папку Музыка
        self.after(0, self.перебор) # продолжаем перебор
    def ккласс0(self, event): # последовательность действий для команды класс0 — Удалить
        mixer.music.load('/01.mp3') #предпроигрыш для освобождения трека        
        if способ ==1: #если способ № 1
            папка = Path(self.музыка).stem #определяем название целевой папки по имени демо-трека
            shutil.rmtree("/Музыка/Приёмка/"+папка) #удаляем всю папку (с названием демо-трека) с файлами
        Path(self.музыка).unlink() # удаляем сам трек / демо-трек
        self.after(0, self.перебор) # продолжаем перебор
    def перемотка(self, event): # последовательность действий для команды Перемотка 
        try:
            mixer.music.set_pos(self.n) # сместить позицию воспроизведения
        except: pass
        self.n+=30 # на 30 секунд вперед
app = App(песни)
app.перебор()
app.пуск() # запускаем приложение

#if способ ==2: # Удаление папок в Зачистке
#    for папка in Path('/Музыка/Зачистка').iterdir(): #для всех подпапок в папке «Приёмка»
#        if папка.is_dir() == True: # если папка
#            shutil.rmtree(папка) # удалить папку с файлами
