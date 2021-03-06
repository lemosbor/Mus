from bs4 import BeautifulSoup # импорт класса BeautifulSoup из модуля bs4
import requests # модуль для веб-запросов
import json # модуль для работы с json
import re # модуль для работы с текстом
import webbrowser # модуль для работы с ссылками
import time # модуль для работы со временем
import mouse # модуль для имитации мышки
from fp.fp import FreeProxy # модуль выгрузки прокси https://pypi.org/project/free-proxy/


def парсинг(адрес): # задаем функцию Парсинг, предварительно выгрузив прокси # ВОЗМОЖНО нужен метод конструктора
	global проксиадрес
	global суп
	while True: # запускаем цикл перебора проксиадресов
		try: # пробуем обратиться по текущему проксиадресу
			запрос = requests.get(адрес, proxies={'http': проксиадрес, 'https': проксиадрес}) # делаем запрос к сайту, используя прокси
			запрос.encoding = 'utf-8' #перекодируем результат запроса для корректного отображения кириллици
			суп = BeautifulSoup(запрос.text,  'html.parser') # 'lxml' создаем объект BeautifulSoup (суп) и передаём его конструктору. Вторая опция уточняет объект парсинга.
			break # завершаем цикл
		except: # если возникла ошибка (нет доступа через текущий прокси)
			print("Не удолось подключиться с прокси:", проксиадрес, "Продолжаем.") #сообщаем
			проксиадрес = FreeProxy(rand=True).get() # выгружаем другой прокси	
проксиадрес = FreeProxy(rand=True).get() # выгружаем рабочий прокси
# ПАРСИНГ ЗАПИСЕЙ
итерация=1 # номер страницы
while True: # цикл перебора страниц
	if итерация == 1: адрес ="https://funkysouls.org/music/index.html" # для первой страницы		
	else: адрес =("https://funkysouls.org/music/page/"+str(итерация)+".html") # для последующих		
	база = json.loads(open ('музыка.json', "r", encoding='utf-8').read()) # открываем базу
	альбомы = [i['а'] for i in база] # создаем перечень существующих записей (альбомов)
	предбаза = [] # создаем пустую предбазу
	парсинг(адрес) # запускаем функцию парсинга по адресу для получения супа
	массив = суп.find_all("h2") # из супа формируем массив записей с тегом <h2>
	альбом = [м.text for м in массив if м.text is not None] # формируем список названий (text) из массива
	массивссылок = суп.find_all("p", class_="download_box") # из супа формируем массив ссылок с тегом <р> и с классом download_box
	ссылки = [м.a['href'] for м in массивссылок if м.a['href'] is not None] # формируем список ссылок (элемент href) из массива ссылок
	for i, n in zip(альбом, ссылки): # объединение списков названий и ссылок по ключам
		предбаза.append({'а' : i, 'ф' : n}) # добавляем в подбазу название альбома (а) и ссылку на форум (ф)
	предбаза = [i for i in предбаза if not (i["а"] in альбомы)] #удаляем из предбазы существующие альбомы (из перечня альбомы)
	база = база + предбаза # добавляем записи в базу
	with open("музыка.json", "w", encoding='utf-8') as i: i.write(json.dumps(база, ensure_ascii = False)) # записываем базу
	print("Добавленно альбомов:", len(предбаза))
	итерация +=1 # переходим к следующей странице
	if len(предбаза) < 14: break # если записалось меньше 14 альбомов, то мы достигли конца и пора прекращать цикл
# ПАРСИНГ ФОРУМА (поиск ссылок на файлы-архивы)
база = json.loads(open ('музыка.json', "r", encoding='utf-8').read()) # открываем базу
for i in база: # прогоняем по всем записям
	if "ссылка" not in i: # если нет ссылки на файл-архив
		адрес = i['ф'] # задаем адрес — ссылка на форум
		назв = i['а'] # задаем название альбома
		print("Парсим форум по альбому:", назв, адрес)		
		парсинг(адрес)
		# Способ 1		
		номер = "p"+(адрес.split('p/')[1]) # номер сообщения на форуме (индекс «р» + часть адреса. разделение по индексу p/)	
		сообщение = суп.find("div", id=номер) # находим код с тегом div и id номера сообщения
		ссылка = сообщение.find('div', class_='text').find_all(string=re.compile('zippyshare.com')) # в сообщении находим тег div с классом text, а в нём находим ссылку по ключевому слову		
		if len(ссылка) > 0: # если ссылка есть (найдена)
			ссылка = ссылка[0] # извлекаем ссылку из массива ссылок (она там одна)
			print("Найденная по Способу 1 ссылка:", ссылка) # сообщаем
		else: # если ссылка не нашлась, то приступаем к Способу 2:
			print("Прямая ссылка не найдена. Ищем ссылки в записях форума")
			файлообменники = ["zippyshare.com", "yadi.sk", "cloud.mail", "file-upload.com", "sendfile.su"] # перечисляем файлообменники, которые нас интересуют
			for k in файлообменники: # перебор для каждого шаблона файлообменника
				позиция0=(str(суп).rfind(k)) # # находим в супе позицию упоминания файлообменника с конца. Вариант: re.findall("......zippyshare.com....", суп)[-1]
				if позиция0 > 0: # если позиций найдена (если не найдена, то позиция будет равна -1).					
					смещение = 0 # задаём смещение относительно позиции
					if k == "zippyshare.com": смещение = 7 # для zippyshare (доменное имя второго уровня) необходимо сместить шаблон, чтобы уместить доменное имя третьего уровня 
					подсуп = str(суп)[(позиция0-смещение):] # обрезаем код страници с позиции0
					подсуп = re.sub('[#% !@\[*\]|"<?]','Ж',подсуп) #заменяем вероятные символы окончая ссылки (в том числе пробел) на символ Ж
					позиция2=подсуп.find("Ж") # позиция первого вхождения Ж в подсупе — окончание адреса ссылки
					ссылка = подсуп[:позиция2] # обрезаем обрезанный код до позиции2 — получаем чистую ссылку
					print("Найденная на форуме ссылка:", ссылка) # сообщаем
					break # прекращаем перебор файлообменников
		i.update({'жанр' : [] }) # задаём список жанров для записи
		for жанр in суп.find_all("a", class_="ftag"): # находим все жанры
			i["жанр"].append(жанр.text) # записываем все жанры в список жанров
		спасибо = суп.find("div", id=номер).find('p', class_='thanx') # поиск количества сказавших спасибо
		i.update({'р' : (спасибо.findChildren()[2].text)}) #записываем количество сказавших спасибо
		if len(ссылка) > 0: i.update({'ссылка' : ссылка}) # если ссылка нашлась, то записывем её
		with open("музыка.json", "w", encoding='utf-8') as m: m.write(json.dumps(база, ensure_ascii = False)) # сохраняем запись в базе
# ОТКРЫВАТЕЛЬ
print("Приступаем к открытию ссылок.")
база = json.loads(open ('музыка.json', "r", encoding='utf-8').read()) # открываем базу
for i in база: # для записи в массиве записей
	if "ссылка" in i and "скачен" not in i: # если в записи есть ссылка, но нет индекса «скачен»
		if '//' not in i['ссылка']: # если в ссылки нет указаня протокола передачи https://
			webbrowser.open('https://' + i['ссылка']) # синтезируем протокол передачи и ссылку, чтобы открывалась в браузере по-умолчанию
		else: webbrowser.open(i['ссылка']) # иначе просто открываем ссылку
		time.sleep(4) # ждём 4 сек
		mouse.move(900,  300, absolute=True, duration=0.2) # переводим указатель мыши в позицию 900, 300
		mouse.click('left') # делаем левый клик мыши (для закачки)
		i.update({'скачен' : 1}) # записываем тег «скачен»
		print(i['а'], "ссылка открыта. Дан тег «скачен».")
	with open("музыка.json", "w", encoding='utf-8') as i: i.write(json.dumps(база, ensure_ascii = False)) # сохраняем базу