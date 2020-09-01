from pydub import AudioSegment # подключаем библиотеку для работы с mp3
from pydub.playback import play # подключаем библиотеку для воспроизведения mp3
import json
song = AudioSegment.from_mp3("01.mp3") # подгружаем mp3 файл
first_10_seconds = song[:10000] # вырезаем первые 10 сек
first_30 = song[30000:35000] # с 30 по 35 сек
last_5_seconds = song[-5000:] # вырезаем последние 5 сек
целая = first_10_seconds + last_5_seconds # объединяем обрезки
целая.export("mashup.mp3", format="mp3") # записываем новый mp3

песни = []
демо = ""
for i in песни:
  песня = AudioSegment.from_mp3(i) # подгружаем mp3 файл
  обрезок = песня[30000:35000]
  демо = демо + обрезок
  # демо = демо.append(обрезок, crossfade=1500) # с плавным переходом
#демо = демо.fade_in(2000).fade_out(3000) # плавное начало и конец
демо.export("демо.mp3", format="mp3", tags={'artist': 'Артист', 'album': 'Альбом', 'song': 'Демо'})
play(демо)
