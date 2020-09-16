import vk_api
from vk_api.audio import VkAudio # модуль ВК
import json # модуль для работы с json
import re # модуль работы с текстом
import requests # модуль запросов к инету

база = json.loads(open ('постыВК.json', "r", encoding='utf-8').read()) # открываем базу
#Парсинг стены:
#ВЫГРУЗКА
предбаза = [i for i in выгрузка if not (i["id"] in база)] #удаляем из предбазы существующие альбомы
база = база + предбаза # добавляем записи в базу
with open("постыВК.json", "w", encoding='utf-8') as i: i.write(json.dumps(база, ensure_ascii = False)) # записываем базу
print("Добавленно альбомов:", len(предбаза))

вксессия = vk_api.VkApi('+79162863084', 'L-02') # задаём параметры авторизации
вксессия.auth() # авторизируемся
for альбом in предбаза:
	try:
		песни = VkAudio(вксессия, convert_m3u8_links=True).get_post_audio(-80472434,альбом) # выгружаем песни из поста
		#создать папку с альбомом
		for песня in list(песни): # для песни из листа песен поста
			выгрузкапесни = requests.get(песня['url'].split("?")[0]) #получаем адрес для выгрузки песни (обрезаем по знаку «?»), выгружаем
			with open('/Users/Илья/Music/Приёмка/'+альбом+'/'+песня['title']+'.mp3', 'wb') as f:   #записываем в файл с названием песни
				f.write(выгрузкапесни.content)  #содержимое песни
	except: pass
