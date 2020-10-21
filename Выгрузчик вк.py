import vk_api
from vk_api.audio import VkAudio # модуль ВК
import json # модуль для работы с json
import re # модуль работы с текстом
import os
import requests # модуль запросов к инету
from mutagen.mp3 import EasyMP3

def описание(file_name, title, artist):
	try:
		tags = EasyMP3(file_name)
		tags["title"] = title
		tags["artist"] = artist
		tags.save()
	except: pass

вксессия = vk_api.VkApi('+79162863084', '') # задаём параметры авторизации
вксессия.auth() # авторизируемся
база = json.loads(open ('постыВК.json', "r", encoding='utf-8').read()) # открываем базу
сообщество = -80472434
#Парсинг стены:
vk = вксессия.get_api() #выгрузка класса обращения к методам API 
выгрузка=vk.wall.get(owner_id=сообщество, count=25)["items"] #выгружаем 20 запесей со стены стену
выгрузка= [пост['id'] for пост in выгрузка] #создаем список постов из выгрузки
предбаза = [пост for пост in выгрузка if not (пост in база)] #удаляем из предбазы существующие посты
база = база + предбаза # добавляем записи в базу
with open("постыВК.json", "w", encoding='utf-8') as i: i.write(json.dumps(база, ensure_ascii = False)) # записываем базу
print("Добавленно постов:", len(предбаза))
#предбаза=[92918]
for пост in предбаза:
#	try:
	песни = VkAudio(вксессия, convert_m3u8_links=True).get_post_audio(сообщество,пост) # выгружаем песни из поста
	п = 0
	os.mkdir('/Музыка/Приёмка/'+str(пост)) #создаем папку поста
	for песня in list(песни): # для песни из листа песен поста
		выгрузкапесни = requests.get(песня['url'].split("?")[0]) #получаем адрес для выгрузки песни (обрезаем по знаку «?»), выгружаем
		название = re.sub("[#%!@*?/]", "", песня['title'])
		исполнитель = песня['artist']
		адрес='/Музыка/Приёмка/'+str(пост)+'/'+название+'.mp3'
		with open(адрес, 'wb') as f:   #записываем в файл с названием песни
			f.write(выгрузкапесни.content)  #содержимое песни
		описание(адрес, название, исполнитель)
		п += 1
	if п==0:
		os.rmdir('/Музыка/Приёмка/'+str(пост))
#except: pass
