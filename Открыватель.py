import webbrowser
import json

база = json.loads(open ('музыка.json', "r", encoding='utf-8').read()) # открываем базу
for i in база: # прогоняем по всем записям
	if "ссылка" in i and "скачен" not in i: # если нет ссылки
		webbrowser.open(i['ссылка'])
		i.update({'скачен' : 1})
	with open("музыка.json", "w", encoding='utf-8') as i: i.write(json.dumps(база, ensure_ascii = False)) # записываем базу