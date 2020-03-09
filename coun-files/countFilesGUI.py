import PySimpleGUI as sg
import sys
import os
import json

# the setting
try:
    with open('icon/setting.txt', 'r', encoding='utf-8') as f:
        setting = json.load(f)
except Exception as e:
    setting = {'lang':'EN'}
    with open('icon/setting.txt', 'w', encoding='utf-8') as f:
        json.dump(setting, f)

# import lang form and return LF = dict
sys.path.append("icon\\")
if setting['lang'] == 'RU':
    from lang_ru import *
else:
    from lang_en import *

def p(text, *args):
    print(text, *args, sep = ' / ', end = '\n')

# returns True on the reserved extension, may return the extension itself
def fexpansion(path, exps = list):
    for exp in exps:
        if path.endswith(exp.strip()):
            return True
    return False

# returns known file encoding
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
    sg.theme('Dark')   # Add a touch of color
    sg.SetOptions(auto_size_buttons=False)
    # Menu Definition
    menu_def = [[LF['CF_MENU_FILE'], [LF['CF_MENU_LANG'], ['EN','RU'], LF['CF_MENU_EXIT']+'::_exit_']],[LF['CF_MENU_HELP'], LF['CF_MENU_ABOUT_LINK']+'::_about_']]
    # All the stuff inside your window.
    layout = [  # the form
                [sg.Menu(menu_def, tearoff=True)],
                [sg.Text(LF['CF_EXPANSION'], size=(18, 1)), sg.InputText(default_text=expansion, key='_expansion_')],
                [sg.Text(LF['CF_PATH'], size=(18, 1)), sg.InputText(key='_path_'), sg.FolderBrowse(LF['CF_PATH_BUTTON'], key='_browse_')],
                [sg.Multiline(default_text=LF['CF_MESSAGE'], size=(80, 5), key='_message_', autoscroll=True)],
                [sg.Button(LF['CF_RUN'], key='_ok_'), sg.Button(LF['CF_CLOSE'], key='_cansel_')] ]

    # Create the Window
    window = sg.Window(LF['CF_TITLE'], layout, icon = favicon)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        errorForm = []
        if event in (None, '_cansel_'):   # if user closes window or clicks cancel
            break    
        
        if event.find('_about_') > 0:
            sg.PopupScrolled(LF['CF_MENU_ABOUT'], size=(60, None), no_titlebar=True)

        if event.find('_exit_') > 0:
            window.close()

        if event == 'EN' or event == 'RU':
            setting = {'lang':event}
            with open('icon/setting.txt', 'w', encoding='utf-8') as f:
                json.dump(setting, f)
            window.close()

        if event == '_ok_':
            # validation
            if len(values['_path_']) == 0:
                errorForm.append(LF['CF_ERROR_PATH']) 
            if len(values['_expansion_']) == 0:
                errorForm.append(LF['CF_ERROR_EXPANSION'])
            
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
                mList = [LF['CF_FILES'] + str(len(farr)), LF['CF_SIZE'] + str(round(skb, 2)) + ' kB', LF['CF_LINES'] + str(sm)]
                window['_message_'].update(" / ".join(mList)+'\n', append=True)                
                #window.Refresh()             

    window.close()

if __name__ == '__main__':
    main()