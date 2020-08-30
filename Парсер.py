from bs4 import BeautifulSoup
import requests as req
import json
import re
# ПАРСИНГ ЗАПИСЕЙ
конец=0 # индикатор окончания просмотра страниц
итерация =1 # первая страница
while конец==0: # цикл перебора страниц
	if итерация ==1: # для первой страницы
		адрес ="https://funkysouls.org/music/index.html"
	else: # для последующих
		адрес =("https://funkysouls.org/music/page/"+str(итерация)+".html")
	база = json.loads(open ('музыка.json', "r", encoding='utf-8').read()) # открываем базу
	альбомы = [i['а'] for i in база] # задаем перечень существующих записей (альбомов)
	предбаза = [] # создаем пустую предбазу
	proxies = { 'http': "http://83.97.23.90:18080", 'https': "http://83.97.23.90:18080"} # задаем прокси (для заблокированных сайтов)
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
	if len(предбаза) < 14: # если записалось меньше 14 альбомов, то мы достигли конца и пора прекращать цикл
		конец = 1
# ПАРСИНГ ФОРУМА
база = json.loads(open ('музыка.json', "r", encoding='utf-8').read())
for i in база:
	if "ссылка" not in i:
		адрес = i['ф']
		print(адрес)
		номер = "p"+(адрес.split('p/')[1])
		resp = req.get(адрес, proxies=proxies) # делаем запрос к сайту, используя прокси
		resp.encoding = 'utf-8' #перекодируем результат запроса
		суп = BeautifulSoup(resp.text,  'lxml') # формируем читаемый текст
		сообщение = суп.find("div", id=номер)
		ссылка = сообщение.find('div', class_='text').find_all(string=re.compile('zippyshare')) #поиск ссылки
		for txt in ссылка:
			#print(" ".join(txt.split()))
			i.update({'ссылка' : " ".join(txt.split())})
		i.update({'жанр' : [] })
		for жанр in суп.find_all("a", class_="ftag"): # поиск жанра
		        #print(жанр.text)		    
		    i["жанр"].append(жанр.text)
		спасибо = суп.find("div", id=номер).find('p', class_='thanx') # поиск спасибо
		i.update({'р' : (спасибо.findChildren()[2].text)})
		with open("музыка.json", "w", encoding='utf-8') as i: i.write(json.dumps(база, ensure_ascii = False)) # записываем базу