import os
import json
import requests
from io import BytesIO
from itertools import cycle
import tkinter as tk # Python3

инфо = [1, 2, 3, 4, 5]

class App(tk.Tk): #'''Tk window/label adjusts to size of image'''
    def __init__(self, инфо): # the root will be self
        tk.Tk.__init__(self)# allows repeat cycling through the pictures # store as (img_object, img_name) tuple
		self.инфоцикл = cycle(info for info in инфо) #выгружаем информацию из списка информации
        self.текстовка = tk.Label(self) #задаём область для текста
        self.текстовка.pack()
    def перебор(self): # собственно перебор фоторафий
        self.инфо= next(self.инфоцикл) #отображаемая информация
        self.title(self.инфо) #область айди (титул)
        self.текстовка.config(text=self.инфо) #область текстовки с информцией
        self.bind('<Left>', self.ккласс0) # если жмём кнопку 0, то вызываем команду класс0
        self.bind('<Right>', self.ккласс1) # если жмём кнопку +, то вызываем команду класс0
        #self.bind('<space>', self.на_доп) # если жмём кнопку вправо, то вызываем команду на_доп
    def пуск(self): #запускаем панель
        self.mainloop()
    def ккласс1(self, event): #команда класс1
        #Оставляем
        self.after(0, self.перебор) # запускаем перебор
    def ккласс0(self, event): #команда класс0
        #Удаляем
        self.after(0, self.перебор) # запускаем перебор
app = App(инфо)
app.перебор()
app.пуск() # запускаем приложение
#пав