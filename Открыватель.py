import webbrowser # библиотека работы с ссылками
import json
import time

база = json.loads(open ('музыка.json', "r", encoding='utf-8').read()) # открываем базу
for i in база: # для записи в массиве записей
	if "ссылка" in i and "скачен" not in i: # если в записи есть ссылка, но нет индекса «скачен»
		webbrowser.open(i['ссылка']) # открыть ссылку
		time.sleep(0.8)
		#ПОСПАТЬ
		i.update({'скачен' : 1}) # записать индекс "скачен"
	with open("музыка.json", "w", encoding='utf-8') as i: i.write(json.dumps(база, ensure_ascii = False)) # записываем базу
