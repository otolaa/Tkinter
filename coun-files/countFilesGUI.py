import PySimpleGUI as sg
import sys
import os

def p(text, *args):
    print(text, *args, sep = ' / ', end = '\n')

# возвращает True на зарезервированное расширение, может возвращать само расширение 
def fexpansion(path, exps = list):
    for exp in exps:
        if path.endswith(exp.strip()):
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
            break
    return encodingCod

def main():
    favicon = "icon\\favicon.ico" # the icon from windows
    expansion = '.php, .less, .scss' # file extension
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  # the form
                [sg.Text('Расширение файлов:', size=(18, 1)), sg.InputText(default_text=expansion, key='_expansion_')],
                [sg.Text('Выберите папку:', size=(18, 1)), sg.InputText(key='_path_'), sg.FolderBrowse('Выбрать', key='_browse_')],
                [sg.Multiline(default_text='Сообщения:\n', size=(75, 5), key='_message_', autoscroll=True)],
                [sg.Button('Выполнить', key='_ok_'), sg.Button('Закрыть', key='_cansel_')] ]

    # Create the Window
    window = sg.Window('Подсчет количества строк кода', layout, icon = favicon)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        errorForm = []
        if event in (None, '_cansel_'):   # if user closes window or clicks cancel
            break    
        if event == '_ok_':
            # validation
            if len(values['_path_']) == 0:
                errorForm.append('выберите папку') 
            if len(values['_expansion_']) == 0:
                errorForm.append('добавьте расширение файлов')
            
            if len(errorForm) > 0:
                sg.popup("\n".join(errorForm), icon = favicon, no_titlebar=True) 
            else:
                farr = []
                sm = 0
                skb = 0
                for dir, dirs, files in os.walk(values['_path_']):
                    dir = os.path.abspath(dir)              
                    for f in files:
                        if not fexpansion(f, values['_expansion_'].split(',')):
                            continue
                        # возвращает нормализованный абсолютный путь.
                        path = os.path.join(dir, f)
                        # размер файла в kбайтах, округление до второго знака
                        kb = round(os.path.getsize(path)/1024, 2)
                        # если проникнуться дзеном пайтона, то подсчитать количество строк в файле можно так:
                        # генератор списка с условием, выбираем строки только те которые больше 5-ти символов, '<?php'
                        encodingCod = correct_encoding(path) # определаем кодировку файла
                        s = sum(1 for line in open(path, 'r', encoding = encodingCod) if len(line) > 5)
                        # формируем сообщение и т.д.       
                        mList = [str(path), str(encodingCod), str(kb) + ' kB', str(s)]               
                        window['_message_'].update(" / ".join(mList)+'\n', append=True)
                        # добавляет записи в список, для подсчета количества файлов
                        farr.append(path)
                        sm += s  # количество строк, += сложение и присваивание
                        skb += kb # количество кбайт, += сложение и присваивание                   
                mList = ['Количество файлов: ' + str(len(farr)), 'Размер: ' + str(round(skb, 2)) + ' kB', 'Всего строк кода: ' + str(sm)]
                window['_message_'].update(" / ".join(mList)+'\n', append=True)                
                #window.Refresh()             

    window.close()

if __name__ == '__main__':
    main()