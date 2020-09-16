import vk_api
from vk_api.audio import VkAudio # модуль ВК
import json # модуль для работы с json
import re # модуль работы с текстом
import os
import requests # модуль запросов к инету

сообщество = -80472434

база = json.loads(open ('постыВК.json', "r", encoding='utf-8').read()) # открываем базу
#Парсинг стены:
#ВЫГРУЗКА
выгрузка= [пост['id'] for пост in выгрузка] #создаем список постов из выгрузки
предбаза = [пост for пост in выгрузка if not (пост in база)] #удаляем из предбазы существующие посты
база = база + предбаза # добавляем записи в базу
with open("постыВК.json", "w", encoding='utf-8') as i: i.write(json.dumps(база, ensure_ascii = False)) # записываем базу
print("Добавленно постов:", len(предбаза))

вксессия = vk_api.VkApi('+79162863084', 'L-02') # задаём параметры авторизации
вксессия.auth() # авторизируемся
for пост in предбаза:
	try:
		песни = VkAudio(вксессия, convert_m3u8_links=True).get_post_audio(сообщество,пост) # выгружаем песни из поста
		os.mkdir('/Users/Илья/Music/Приёмка/'+пост) #создаем папку поста
		for песня in list(песни): # для песни из листа песен поста
			выгрузкапесни = requests.get(песня['url'].split("?")[0]) #получаем адрес для выгрузки песни (обрезаем по знаку «?»), выгружаем
			with open('/Users/Илья/Music/Приёмка/'+пост+'/'+песня['title']+'.mp3', 'wb') as f:   #записываем в файл с названием песни
				f.write(выгрузкапесни.content)  #содержимое песни
	except: pass
