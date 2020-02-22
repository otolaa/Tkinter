# подсчет файлов с определенным расширении в определенной папке
# модуль os https://pythonworld.ru/moduli/modul-os-path.html
import sys
import json # сохраняем все в json
import os

def p(text, *args):
    print(text, *args, sep = ' / ', end = '\n')

# возвращает True на зарезервированное расширение, может возвращать само расширение 
def fexpansion(path):
    for exp in ['.php', '.less', '.scss']:
        if path.endswith(exp):
            return True
    return False

# возвращает известную кодировку файла
def correct_encoding(path):
    encodingList = ['utf-8', 'windows-1251', 'cp500', 'utf-16', 'GBK', 'ASCII', 'US-ASCII', 'Big5']
    encodingCod = ''
    for enc in encodingList:
        try:
            open(path, encoding = enc).read()
        except (UnicodeDecodeError, LookupError):
            pass
        else:
            encodingCod = enc
            # print('Кодировка файла -- ' + encodingCod + ' ' + path)
            break
    return encodingCod

def main():
    src = "d:\\OSPanel\\domains\\westpower\\infosystems\\local\\templates\\infosystems\\"
    farr = []
    sm = 0
    skb = 0
    for dir, dirs, files in os.walk(src):
        dir = os.path.abspath(dir)
        # p(files)
        for f in files:
            if not fexpansion(f):
                continue
            # возвращает нормализованный абсолютный путь.
            path = os.path.join(dir, f)
            # размер файла в kбайтах, округление до второго знака
            kb = round(os.path.getsize(path)/1024, 2)
            # если проникнуться дзеном пайтона, то подсчитать количество строк в файле можно так:
            # генератор списка с условием, выбираем строки только те которые больше 5-ти символов, '<?php'
            encodingCod = correct_encoding(path) # определаем кодировку файла
            s = sum(1 for line in open(path, 'r', encoding = encodingCod) if len(line) > 5)           
            p(path, encodingCod, str(kb) + ' kB', s)
            # добавляет записи в список, для подсчета количества файлов
            farr.append(path)
            sm += s  # количество строк, += сложение и присваивание
            skb += kb # количество кбайт, += сложение и присваивание
    # возвращает количество записей в списке, килобайт в файлах, количество строк
    p('Количество файлов: ' + str(len(farr)), 'Размер: ' + str(round(skb, 2)) + ' kB', 'Всего строк кода: ' + str(sm))
    # p(farr)

if __name__ == '__main__':
    main()