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


def main():
    src = "d:\\OSPanel\\domains\\westpower\\infosystems\\local\\php_interface\\"
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
            # генератор списка с условием, выбираем строки только те которые больше 3-x символов
            s = sum(1 for line in open(path, 'r', encoding='utf-8') if len(line) > 3)           
            p(path, kb, s)
            # добавляет записи в список, для подсчета количества файлов
            farr.append(path)
            sm += s  # количество строк, += сложение и присваивание
            skb += kb # количество кбайт, += сложение и присваивание
    # возвращает количество записей в списке, килобайт в файлах, количество строк
    p(len(farr), round(skb, 2), sm)
    # p(farr)

if __name__ == '__main__':
    main()