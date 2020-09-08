from bs4 import BeautifulSoup
import requests as req
import json
import re
import webbrowser # библиотека работы с ссылками
import time
import mouse
# ПАРСИНГ ЗАПИСЕЙ
конец=0 # индикатор окончания просмотра страниц
итерация =1 # первая страница
while конец==0: # цикл перебора страниц
	if итерация ==1: адрес ="https://funkysouls.org/music/index.html" # для первой страницы		
	else: адрес =("https://funkysouls.org/music/page/"+str(итерация)+".html") # для последующих		
	база = json.loads(open ('музыка.json', "r", encoding='utf-8').read()) # открываем базу
	альбомы = [i['а'] for i in база] # задаем перечень существующих записей (альбомов)
	предбаза = [] # создаем пустую предбазу
	про="95.174.67.50"
	кси="18080"
#	proxies = { 'http': "http://83.97.23.90:18080", 'https': "http://176.56.107.238:52184"}
	proxies = { 'http': "http://"+про+":"+кси, 'https': "http://"+про+":"+кси} # задаем прокси (для заблокированных сайтов) https://free-proxy-list.net/
	resp = req.get(адрес, proxies=proxies) # делаем запрос к сайту, используя прокси
	resp.encoding = 'utf-8' #перекодируем результат запроса
	суп = BeautifulSoup(resp.text,  'lxml') # формируем читаемый текст
	массив = суп.find_all("h2") # формируем массив по тегу
	альбом = [м.text for м in массив if м.text is not None] # формируем список названия
	массивссылок = суп.find_all("p", class_="download_box") 
	ссылки = [м.a['href'] for м in массивссылок if м.a['href'] is not None]
	for i, n in zip(альбом, ссылки): # объединение списков по ключам
		предбаза.append({'а' : i, 'ф' : n})
	предбаза = [i for i in предбаза if not (i["а"] in альбомы)] #удаляем из предбазы существующие записи
	база = база + предбаза # добавляем записи в предбазу
	with open("музыка.json", "w", encoding='utf-8') as i: i.write(json.dumps(база, ensure_ascii = False)) # записываем базу
	print("Добавленно альбомов:", len(предбаза))
	итерация +=1
	if len(предбаза) < 14: конец = 1 # если записалось меньше 14 альбомов, то мы достигли конца и пора прекращать цикл		
# ПАРСИНГ ФОРУМА
база = json.loads(open ('музыка.json', "r", encoding='utf-8').read()) # открываем базу
for i in база: # прогоняем по всем записям
	if "ссылка" not in i: # если нет ссылки
		адрес = i['ф'] # адрес — ссылка на форум
		print(адрес) 
		номер = "p"+(адрес.split('p/')[1]) # номер сообщения на форуме (индекс «р» + часть адреса)
		resp = req.get(адрес, proxies=proxies) # делаем запрос к адресу, используя прокси
		resp.encoding = 'utf-8' #перекодируем результат запроса
		суп = BeautifulSoup(resp.text,  'lxml') # формируем читаемый текст
		сообщение = суп.find("div", id=номер) # находим тело сообщения
		ссылка = сообщение.find('div', class_='text').find_all(string=re.compile('zippyshare')) # находим ссылку ДОБАВИТЬ поиск альтернативных систем закачивания
		for txt in ссылка:
			i.update({'ссылка' : " ".join(txt.split())}) # записываем ссылку
		if not "ссылка" in i:
			ссылка = суп.find('div', class_='inner').find_all(string=re.compile('zippyshare')) # находим ссылку ДОБАВИТЬ поиск альтернативных систем закачивания
			for txt in ссылка:
				i.update({'ссылка' : " ".join(txt.split())}) # записываем ссылку
		if not "ссылка" in i:
			ссылка = суп.find('div', class_='inner').find_all(string=re.compile('cloud.mail')) # находим ссылку ДОБАВИТЬ поиск альтернативных систем закачивания
			for txt in ссылка:
				i.update({'ссылка' : " ".join(txt.split())}) # записываем ссылку
		i.update({'жанр' : [] }) # записываем список жанров
		for жанр in суп.find_all("a", class_="ftag"): # находим все жанры
		    i["жанр"].append(жанр.text) # записываем все жанры в список жанров
		спасибо = суп.find("div", id=номер).find('p', class_='thanx') # поиск количества сказавших спасибо ДОРАБОТАТЬ
		i.update({'р' : (спасибо.findChildren()[2].text)}) #записываем количество сказавших спасибо
		with open("музыка.json", "w", encoding='utf-8') as i: i.write(json.dumps(база, ensure_ascii = False)) # записываем базу
# ОТКРЫВАТЕЛЬ
база = json.loads(open ('музыка.json', "r", encoding='utf-8').read()) # открываем базу
for i in база: # для записи в массиве записей
	if "ссылка" in i and "скачен" not in i: # если в записи есть ссылка, но нет индекса «скачен»
		webbrowser.open(i['ссылка']) # открыть ссылку
		time.sleep(4)
		mouse.move(900,  300, absolute=True, duration=0.2)
		mouse.click('left')
		#ПОСПАТЬ
		i.update({'скачен' : 1}) # записать индекс "скачен"
	with open("музыка.json", "w", encoding='utf-8') as i: i.write(json.dumps(база, ensure_ascii = False)) # записываем базу
	
#<div class="body">	<div class="text"> <b><span style='font-size:14pt;line-height:100%'>Jon Gurd</span></b><br><br><a href='https://funkyimg.com/view/36ZUP' target='_blank'><img src='https://funkyimg.com/i/36ZUP.jpeg' alt='картинка, оставленная пользователем'></a><br><br><a href='https://forum.funkysouls.org/go.php?https://jongurd.bandcamp.com/' target='_blank'>bandcamp</a><br><br><b>Jon Gurd – Lion (2020)</b><br><br><a href='https://funkyimg.com/view/36ZUU' target='_blank'><img src='https://funkyimg.com/i/36ZUU.jpg' alt='картинка, оставленная пользователем'></a><br><br>CD1:<br>01 – Love<br>02 – Together<br>03 – Goodbye<br>04 – Lion<br>05 – Star<br>06 – See It<br>07 – District<br>08 – Endless<br>09 – You Are<br>10 – The Dream<br><br>CD2:<br>01 – Together<br>02 – Lion (Edit)<br>03 – The Dream (Edit)<br>04 – District (Edit)<br><br><a href='https://forum.funkysouls.org/go.php?https://www117.zippyshare.com/v/Epi3DSTq/file.html' target='_blank'>MP3</a>   175MB<br><br><a href='https://forum.funkysouls.org/go.php?https://www117.zippyshare.com/v/9Y0CAwcu/file.html' target='_blank'>FLAC</a>   440MB  </div>
