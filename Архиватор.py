from pyunpack import Archive
import json
import os

Проиндексировать файлы в папке с закаченными архивами
для и в проиндексированной папке:
  Archive("Test.7z").extractall(".") # разархивировать
  os.remove("Test.7z") # удалить архив
