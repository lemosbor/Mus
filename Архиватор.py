from pyunpack import Archive # библиотека работы с архивами. Для установки библиотеки необходимо pip install patool, pip install pyunpack (из папки с 7Z) и прописать папку с 7Z в пути Path
import json
import os
import glob # библиотека работы с расширениями
from pathlib import Path # библиотека для работы с папками
архивы = [] # создаем массив архивов
for n in Path(".").glob('*.rar'): # для файлов с расширением *.rar
	архивы.append(n.name) #добавляем имя пути
for n in Path(".").glob('*.7z'): # для файлов с расширением *.7z
	архивы.append(n.name) #добавляем имя пути
for n in Path(".").glob('*.zip'): # для файлов с расширением *.zip
	архивы.append(n.name) #добавляем имя пути
print("Кол-во архивов:", архивы)
for i in архивы: # для каждого архива из массива архивов
	Archive(i).extractall("База") # разархивировать в папку "База"
	os.remove(i) # удалить архив
