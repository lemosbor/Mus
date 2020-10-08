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
	проксиадрес = FreeProxy(country_id=['US', 'NL'], rand=True).get() # выгружаем рабочий прокси
	запрос = requests.get(адрес, proxies={'http': проксиадрес, 'https': проксиадрес}) # делаем запрос к сайту, используя прокси
	запрос.encoding = 'utf-8' #перекодируем результат запроса для корректного отображения кириллици
	суп = BeautifulSoup(запрос.text,  'lxml') # создание объекта BeautifulSoup (суп) и передача его конструктору. Вторая опция уточняет объект парсинга.
	массив = суп.find_all("h2") # из супа формируем массив по тегу h2
	альбом = [м.text for м in массив if м.text is not None] # формируем список названий (text) из массива
	массивссылок = суп.find_all("p", class_="download_box") # из супа формируем массив ссылок по тегу р с классом download_box
	ссылки = [м.a['href'] for м in массивссылок if м.a['href'] is not None] # формируем список ссылок (элемент href) из массива ссылок
	for i, n in zip(альбом, ссылки): # объединение списков названий и ссылок по ключам
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
		print("Парсинг форума по альбому:", назв)
		номер = "p"+(адрес.split('p/')[1]) # номер сообщения на форуме (индекс «р» + часть адреса. разделение по индексу p/)
		запрос = requests.get(адрес, proxies={'http': проксиадрес, 'https': проксиадрес}) # делаем запрос к адресу, используя прокси
		запрос.encoding = 'utf-8' #перекодируем результат запроса
		суп = BeautifulSoup(запрос.text,  'lxml') # создание объекта BeautifulSoup (суп) и передача его конструктору		
		сообщение = суп.find("div", id=номер) # находим код с тегом div и id номера сообщения
		ссылка = сообщение.find('div', class_='text').find_all(string=re.compile('zippyshare.com')) # в сообщении находим тег div с классом text, а в нём находим ссылку по ключевому слову		
		for txt in ссылка:
			i.update({'ссылка' : " ".join(txt.split())}) # записываем ссылку
		if not "ссылка" in i: # если ссылка не нашлась, то находим по-другому
			try:			
				позиция1=[суп.rfind("zippyshare.com")][0]-7 # позиция последнего словосочетания на всей странице - 7 знаков
				подсуп = суп[позиция1:] # обрезаем код страници с позиции1
				позиция2=[подсуп.find("html")][0]+4 # позиция первого словосочетания в подсупе + 4 знака			
				ссылка = подсуп[:позиция2] # обрезаем обрезанный код до позиции2 #ссылка = суп.find_all(string=re.compile('zippyshare.com')) # находим ссылку во всём супе в обратном порядке				
				print("Найдена ссылка:", ссылка)
				i.update({'ссылка' : ссылка}) # записываем ссылку
			except: print("Ссылка не найдена на странице:", адрес)
		i.update({'жанр' : [] }) # записываем список жанров
		try:
			for жанр in суп.find_all("a", class_="ftag"): # находим все жанры
			    i["жанр"].append(жанр.text) # записываем все жанры в список жанров
		except: print("Жанры альбома", назв, "не определены.")
		try:
			спасибо = суп.find("div", id=номер).find('p', class_='thanx') # поиск количества сказавших спасибо ДОРАБОТАТЬ
			i.update({'р' : (спасибо.findChildren()[2].text)}) #записываем количество сказавших спасибо
		except: print("Количество сказавших спасибо за альбом", назв, "не определено.")
		with open("музыка.json", "w", encoding='utf-8') as i: i.write(json.dumps(база, ensure_ascii = False)) # записываем базу
# ОТКРЫВАТЕЛЬ
print("Парсинг завершён. Приступаем к открытию ссылок.")
база = json.loads(open ('музыка.json', "r", encoding='utf-8').read()) # открываем базу
for i in база: # для записи в массиве записей
	if "ссылка" in i and "скачен" not in i: # если в записи есть ссылка, но нет индекса «скачен»
		webbrowser.open(i['ссылка']) # открыть ссылку в браузере
		time.sleep(4) # подождать 4 сек
		mouse.move(900,  300, absolute=True, duration=0.2) # перевести указатель мыши в позицию 900, 300
		mouse.click('left') # левый клик мыши
		i.update({'скачен' : 1}) # записать индекс "скачен"
		print(i['а'], "скачен.")
	with open("музыка.json", "w", encoding='utf-8') as i: i.write(json.dumps(база, ensure_ascii = False)) # записываем базу
