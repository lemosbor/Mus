from pyunpack import Archive # библиотека работы с архивами. Для установки библиотеки необходимо pip install patool, pip install pyunpack (из папки с 7Z) и прописать папку с 7Z в пути Path
from pathlib import Path # библиотека для работы с папками
import os
from pydub import AudioSegment # подключаем библиотеку для работы с mp3
#from pydub.playback import play # подключаем библиотеку для воспроизведения mp3

архивы = [] # создаем массив архивов
for n in Path("/Users/Илья/Downloads").glob('*.rar'): # для файлов с расширением *.rar ПОПРОБОВАТЬ сделать список
	архивы.append(str(n)) #добавляем имя пути
for n in Path("/Users/Илья/Downloads").glob('*.7z'): # для файлов с расширением
	архивы.append(str(n)) #добавляем имя пути
for n in Path("/Users/Илья/Downloads").glob('*.zip'): # для файлов с расширением 
	архивы.append(str(n)) #добавляем имя пути
print("Кол-во архивов:", len(архивы))
for i in архивы: # для каждого архива из массива архивов
	Archive(i).extractall("/Users/Илья/Music/Приёмка") # разархивировать в папку «Приёмка»
	os.remove(i) # удалить архив
# НАРЕЗЧИК
for папка in Path('/Users/Илья/Music/Приёмка').iterdir(): #для всех подпапок в папке «Приёмка»
	демо = 0 #создаём демо-трек
	for n in Path(папка).glob('*.mp3'): # в каждом файле с расширением mp3 рассматриваемой папки
		песня = AudioSegment.from_mp3(n) # подгружаем файл
		обрезок = песня[63000:70000].fade_in(1000).fade_out(500) + песня[95000:102000].fade_in(500).fade_out(1500) # создаем обрезок песни с 1:03—1:10 и 1:35—1:42 с затуханием
		демо = демо + обрезок # формируем демо-трек
	демо.export("/Users/Илья/Music/"+(папка.name)+".mp3", format="mp3", tags={'artist': папка.name}) # записываем демо-трек с именем и тегом по названию папки
