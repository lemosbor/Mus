from pydub import AudioSegment # подключаем библиотеку для работы с mp3
from pydub.playback import play # подключаем библиотеку для воспроизведения mp3
import json
import os
import glob
from pathlib import Path
#for root, dirs, files in os.walk("."):  
папки = []
for root, dirs, files in os.walk("."):  
	папки = папки + dirs

#for root, dirs in os.walk("."):
#  альбомы = root
print(папки)
for i in папки:
	демо = 0
	for n in Path(i).glob('*.mp3'):
		песня = AudioSegment.from_mp3(n) # подгружаем mp3 файл
		#обрезок = 0
		обрезок = песня[63000:70000].fade_in(1000).fade_out(500) + песня[95000:101000].fade_in(500).fade_out(1500)
		#обрезок=обрезок.append(песня[63000:70000] , crossfade=1500)
		#обрезок=обрезок.append(песня[95000:101000] , crossfade=1500)
		демо = демо + обрезок
    	# демо = демо.append(обрезок, crossfade=1500) # с плавным переходом
  		#демо = демо.fade_in(2000).fade_out(3000) # плавное начало и конец
	демо.export(i+"демо.mp3", format="mp3", tags={'artist': i})