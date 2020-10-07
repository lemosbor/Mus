from bs4 import BeautifulSoup # импорт класса BeautifulSoup из модуля bs4
import requests # модуль для веб-запросов
import json # модуль для работы с json
import re # модуль для работы с текстом
import webbrowser # модуль для работы с ссылками
import time # модуль для работы со временем
import mouse # модуль для имитации мышки
from fp.fp import FreeProxy # модуль выгрузки прокси https://pypi.org/project/free-proxy/
# ПАРСИНГ ЗАПИСЕЙ
конец=0 # индикатор окончания просмотра страниц
итерация=1 # первая страница
while конец == 0: # цикл перебора страниц
	if итерация == 1: адрес ="https://funkysouls.org/music/index.html" # для первой страницы		
	else: адрес =("https://funkysouls.org/music/page/"+str(итерация)+".html") # для последующих		
	база = json.loads(open ('музыка.json', "r", encoding='utf-8').read()) # открываем базу
	альбомы = [i['а'] for i in база] # создаем перечень существующих записей (альбомов)
	предбаза = [] # создаем пустую предбазу
	
	# для запросов к заблокированным сайтам
	#про="95.174.67.50" # IP прокси https://free-proxy-list.net/
	#кси="18080" # порт прокси
	#прокси = { 'http': "http://"+про+":"+кси, 'https': "http://"+про+":"+кси} # задаем прокси (для заблокированных сайтов)
	прокси = FreeProxy().get()
	
	запрос = requests.get(адрес, proxies=прокси) # делаем запрос к сайту, используя прокси
	запрос.encoding = 'utf-8' #перекодируем результат запроса
	суп = BeautifulSoup(запрос.text,  'lxml') # создание объекта BeautifulSoup (суп) и передача его конструктору. Вторая опция уточняет объект парсинга.
	массив = суп.find_all("h2") # из супа формируем массив по тегу h2
	альбом = [м.text for м in массив if м.text is not None] # формируем список названий (text) из массива
	массивссылок = суп.find_all("p", class_="download_box") # из супа формируем массив ссылок по тегу р с классом download_box
	ссылки = [м.a['href'] for м in массивссылок if м.a['href'] is not None] # формируем список ссылок (элемент href) из массива ссылок
	for i, n in zip(альбом, ссылки): # объединение списков по ключам
		предбаза.append({'а' : i, 'ф' : n}) # добавляем в подбазу название альбома (а) и ссылку на форум (ф)
	предбаза = [i for i in предбаза if not (i["а"] in альбомы)] #удаляем из предбазы существующие альбомы (из перечня альбомы)
	база = база + предбаза # добавляем записи в базу
	with open("музыка.json", "w", encoding='utf-8') as i: i.write(json.dumps(база, ensure_ascii = False)) # записываем базу
	print("Добавленно альбомов:", len(предбаза))
	итерация +=1
	if len(предбаза) < 14: конец = 1 # если записалось меньше 14 альбомов, то мы достигли конца и пора прекращать цикл		
# ПАРСИНГ ФОРУМА (поиск ссылок на файлы-архивы)
база = json.loads(open ('музыка.json', "r", encoding='utf-8').read()) # открываем базу
for i in база: # прогоняем по всем записям
	if "ссылка" not in i: # если нет ссылки на файл-архив
		адрес = i['ф'] # адрес — ссылка на форум
		назв = i['а'] # название альбома
		print(назв, адрес)
		номер = "p"+(адрес.split('p/')[1]) # номер сообщения на форуме (индекс «р» + часть адреса. разделение по индексу p/)
		запрос = requests.get(адрес, proxies=прокси) # делаем запрос к адресу, используя прокси
		запрос.encoding = 'utf-8' #перекодируем результат запроса
		суп = BeautifulSoup(запрос.text,  'lxml') # создание объекта BeautifulSoup (суп) и передача его конструктору		
		сообщение = суп.find("div", id=номер) # находим код с тегом div и id номера сообщения
		ссылка = сообщение.find('div', class_='text').find_all(string=re.compile('zippyshare.com')) # в сообщении находим тег div с классом text, а в нём находим ссылку по ключевому слову
		print(ссылка)
		for txt in ссылка:
			i.update({'ссылка' : " ".join(txt.split())}) # записываем ссылку
		if not "ссылка" in i: # если ссылка не нашлась, то находим по-другому			
			позиция1=[суп.rfind("zippyshare.com")][0]-7 # позиция словосочетания в супе - 7 знаков
			подсуп = суп[позиция1:]
			позиция2=[подсуп.rfind("html")][0]+4 # позиция словосочетания в подсупе + 4 знака			
			ссылка = подсуп[:позиция2]
			#ссылка = суп.find_all(string=re.compile('zippyshare.com')) # находим ссылку во всём супе в обратном порядке #'https://forum.funkysouls.org/go.php?https://www117.zippyshare.com/v/Epi3DSTq/file.html'
			print(ссылка)
			#for txt in ссылка:
			i.update({'ссылка' : ссылка}) # записываем ссылку
			#print(i['ссылка'])
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
		webbrowser.open(i['ссылка']) # открыть ссылку в браузере
		time.sleep(4) # подождать 4 сек
		mouse.move(900,  300, absolute=True, duration=0.2) # перевести указатель мыши в позицию 900, 300
		mouse.click('left') # левый клик мыши
		i.update({'скачен' : 1}) # записать индекс "скачен"
		print(i['ф'])
	with open("музыка.json", "w", encoding='utf-8') as i: i.write(json.dumps(база, ensure_ascii = False)) # записываем базу
#<div class="body">	<div class="text"> <b><span style='font-size:14pt;line-height:100%'>Jon Gurd</span></b><br><br><a href='https://funkyimg.com/view/36ZUP' target='_blank'><img src='https://funkyimg.com/i/36ZUP.jpeg' alt='картинка, оставленная пользователем'></a><br><br><a href='https://forum.funkysouls.org/go.php?https://jongurd.bandcamp.com/' target='_blank'>bandcamp</a><br><br><b>Jon Gurd – Lion (2020)</b><br><br><a href='https://funkyimg.com/view/36ZUU' target='_blank'><img src='https://funkyimg.com/i/36ZUU.jpg' alt='картинка, оставленная пользователем'></a><br><br>CD1:<br>01 – Love<br>02 – Together<br>03 – Goodbye<br>04 – Lion<br>05 – Star<br>06 – See It<br>07 – District<br>08 – Endless<br>09 – You Are<br>10 – The Dream<br><br>CD2:<br>01 – Together<br>02 – Lion (Edit)<br>03 – The Dream (Edit)<br>04 – District (Edit)<br><br><a href='https://forum.funkysouls.org/go.php?https://www117.zippyshare.com/v/Epi3DSTq/file.html' target='_blank'>MP3</a>   175MB<br><br><a href='https://forum.funkysouls.org/go.php?https://www117.zippyshare.com/v/9Y0CAwcu/file.html' target='_blank'>FLAC</a>   440MB  </div>
