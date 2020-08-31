from pydub import AudioSegment # подключаем библиотеку для работы с mp3
song = AudioSegment.from_mp3("01.mp3") # подгружаем mp3 файл
first_10_seconds = song[:10000] # вырезаем первые 10 сек
last_5_seconds = song[-5000:] # вырезаем последние 5 сек
целая = first_10_seconds + last_5_seconds # объединяем обрезки
целая.export("mashup.mp3", format="mp3") # записываем новый mp3
