import os
from io import BytesIO
from itertools import cycle
import tkinter as tk # Python3
import shutil
from pygame import mixer 
from pathlib import Path
песни = []
способ = 1
for n in Path('/Музыка/Приёмка').glob('*.mp3'):
    песни.append(str(n)) #добавляем имя пути
print(len(песни))
if len(песни) == 0:
    способ = 2
if способ ==1:
    песни = песни
else:
    for папка in Path('/Музыка/Зачистка').iterdir(): #для всех подпапок в папке «Приёмка»
        if папка.is_dir() == True: # есои папка
            for n in Path(папка).glob('*.mp3'):
                песни.append(str(n)) #добавляем имя пути

class App(tk.Tk): #'''Tk window/label adjusts to size of image'''
    def __init__(self, инфо): # the root will be self
        tk.Tk.__init__(self)# allows repeat cycling through the pictures # store as (img_object, img_name) tuple
        self.музыкацикл = cycle(ino for ino in песни)
    def перебор(self): # собственно перебор фоторафий
        self.музыка= next(self.музыкацикл) #отображаемая информация
        self.bind('<Left>', self.ккласс0) # если жмём кнопку 0, то вызываем команду класс0
        self.bind('<Right>', self.ккласс1) # если жмём кнопку +, то вызываем команду класс0
        self.bind('<space>', self.перемотка) # если жмём кнопку вправо, то вызываем команду на_доп
        mixer.init()
        mixer.music.load(self.музыка) # загружаем файл
        mixer.music.play() # запускаем файл
        self.n=30
    def пуск(self): #запускаем панель
        self.mainloop()
    def ккласс1(self, event): #команда класс1
        папка = Path(self.музыка).stem #определяем название целевой папки по имени демо-трека
        mixer.music.load('/01.mp3')
        if способ ==1:
            Path("/Музыка/Приёмка/"+папка).replace("/Музыка/Зачистка/"+папка)
            Path(self.музыка).unlink()
        if способ ==2:
            Path(self.музыка).replace("/Users/Илья/Music/"+Path(self.музыка).name)
        self.after(0, self.перебор) # запускаем перебор
    def ккласс0(self, event): #команда класс0
        mixer.music.load('/01.mp3')
        папка = Path(self.музыка).stem #определяем название целевой папки по имени демо-трека
        if способ ==1:
            shutil.rmtree("/Музыка/Приёмка/"+папка)
        Path(self.музыка).unlink()
        self.after(0, self.перебор) # запускаем перебор
    def перемотка(self, event): #команда класс1
        try:
            mixer.music.set_pos(self.n)
        except: pass
        self.n+=30
app = App(песни)
app.перебор()
app.пуск() # запускаем приложение

if способ ==2:
    for папка in Path('/Музыка/Зачистка').iterdir(): #для всех подпапок в папке «Приёмка»
        if папка.is_dir() == True: # есои папка
            shutil.rmtree(папка)