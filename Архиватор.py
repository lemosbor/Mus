from pyunpack import Archive # библиотека работы с архивами. Для установки библиотеки необходимо pip install patool, pip install pyunpack (из папки с 7Z) и прописать папку с 7Z в пути Path
from pathlib import Path # библиотека для работы с папками
#import os
from pydub import AudioSegment # подключаем библиотеку для работы с mp3

архивы = [] # создаем массив архивов
for n in Path("/Users/Илья/Downloads").glob('*.rar'): # для файлов с расширением *.rar
	архивы.append(str(n)) #добавляем имя пути
for n in Path("/Users/Илья/Downloads").glob('*.7z'): # »
	архивы.append(str(n)) #добавляем имя пути
for n in Path("/Users/Илья/Downloads").glob('*.zip'): # »
	архивы.append(str(n)) #добавляем имя пути
for n in Path("/Users/Илья/Downloads").glob('*.tar'): # »
	архивы.append(str(n)) # добавляем имя пути
if len(архивы) > 0:
	print("Кол-во архивов:", len(архивы))
	for i in архивы: # для каждого архива из массива архивов
		Archive(i).extractall("/Музыка/Приёмка") # разархивировать в папку «Приёмка»
		Path(i).unlink() #os.remove(i) # удалить архив
	print("Архивы распакованны в папку Приёмка и удалены")
else: print("Новых архивов нет")
# НАРЕЗЧИК
print("Приступаем к нарезке демо-треков из папок песен в Приёмке")
существующиедемотреки=[]
for n in Path('/Музыка/Приёмка').glob('*.mp3'):
	существующиедемотреки.append(n.stem)
for папка in Path('/Музыка/Приёмка').iterdir(): #для всех подпапок в папке «Приёмка»
	if папка.is_dir() == True: # если папка
		if папка.name not in существующиедемотреки: #если для них ещё не созданы демо-треки	
	 		демо = 0 #создаём демо-трек
	 		for n in Path(папка).glob('**/*.mp3'): # в каждом файле с расширением mp3 рассматриваемой папки
	 			if Path(n).stat().st_size > 512000: #для файлов размером более 500 кб
	 				песня = AudioSegment.from_mp3(n) # подгружаем файл
	 				обрезок = песня[63000:70000].fade_in(1000).fade_out(500) + песня[95000:102000].fade_in(500).fade_out(1500) # создаем обрезок песни с 1:03—1:10 и 1:35—1:42 с затуханием
	 				демо = демо + обрезок # формируем демо-трек
	 			else: pass
	 		демо.export("/Музыка/Приёмка/"+(папка.name)+".mp3", format="mp3", tags={'artist': папка.name}) # записываем демо-трек с именем и тегом по названию папки
	 		print("Демо-трек для папки", папка.name, "создан")