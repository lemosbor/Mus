from pydub import AudioSegment # подключаем библиотеку для работы с mp3
from pydub.playback import play # подключаем библиотеку для воспроизведения mp3
import json
import os
import glob
from pathlib import Path
#for root, dirs, files in os.walk("."):  
for root, dirs, files in os.walk("."):  
    #for filename in files:
    print(dirs, files)

for root, dirs in os.walk("."):  
  альбомы = dirs
  
for n in альбомы:
  песни = []
  демо = ""
  демо = AudioSegment.from_mp3(n+песни[0])[:5000] #первые пять секунд от первой песни
  for i in Path('/путь альбома').glob('*.mp3'):
    песня = AudioSegment.from_mp3(n+"/"+i) # подгружаем mp3 файл
    обрезок = песня[30000:35000]
    демо = демо + обрезок
    # демо = демо.append(обрезок, crossfade=1500) # с плавным переходом
  #демо = демо.fade_in(2000).fade_out(3000) # плавное начало и конец
  демо.export(n+"демо.mp3", format="mp3", tags={'artist': n})
  play(демо)

# https://github.com/jiaaro/pydub
