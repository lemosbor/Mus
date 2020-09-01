from pyunpack import Archive
import json
import os
import glob
from pathlib import Path
архивы = []
for n in Path(".").glob('*.rar'):
	архивы.append(n.name) #добавляем имя пути
for n in Path(".").glob('*.7z'):
	архивы.append(n.name) #добавляем имя пути
for n in Path(".").glob('*.zip'):
	архивы.append(n.name) #добавляем имя пути

print(архивы)
for i in архивы:
	Archive(i).extractall("База") # разархивировать в папку база
	os.remove(i) # удалить архив
