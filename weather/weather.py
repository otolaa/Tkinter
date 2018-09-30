# парсинг погоды
import sys
import requests
import json
from lxml import html  # для xml для html нужно -- from lxml import html
# import re, cgi
import tkinter as tk
import tkinter.ttk as ttk

class Table(tk.Frame):
    def __init__(self, parent=None, headings=list(), rows=list()):
        tk.Frame.__init__(self, parent)
        #
        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table.tag_configure('grey', background='#e1e1e1', font=("Verdana", 9, 'bold'))
        #
        table["columns"] = headings
        table["displaycolumns"] = headings
        # формируем заголовок таблицы
        for h,head in enumerate(headings):            
            anchor = 'c' if h == 2 or h == 3 or h == 5 else 'w'
            width = 50 if head == 'ID' else 100            
            table.heading(head, text=head, anchor='c')
            table.column(head, width=width, anchor=anchor)
        # формируем значение в cтроках
        for i,row in enumerate(rows):
            s = 0
            for rw in row:
                if s == 0:
                    table.insert('', 'end', text='L'+str(i)+str(s), values=list(rw), tags=('grey'))   
                else:
                    table.insert('', 'end', text='L'+str(i)+str(s), values=list(rw))   
                s+=1        

        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)

def p(text, *args):
    print(text, *args, sep=' / ', end='\n')

# Все обязательные параметры должны быть помещены перед любыми аргументами по умолчанию. Просто потому, что они являются обязательными!
def repleces(text, ls=list()):
    ls = [ls] if type(ls) is str else ls
    for r in ls:
        text = text.replace(r, '')    
    return text.replace(' ', '')

def get_html(url):
    try:
        page = requests.get(url)
        return page.text
    except Exception as e:
        print(sys.exc_info()[1])        
        return False

def isTrue(td5):
    try:
        td5 = td5.xpath('div/span/span')[0].text_content() + " " + td5.xpath('div/div/abbr')[0].attrib["title"]
        return td5
    except Exception as e:
        return td5.text_content()


def parseHTML(html_content):
    # Парсинг HTML
    if html_content == False:
        return False
    #print (html_content)
    root = html.fromstring(html_content)
    # print(root.attrib["class"])
    headers = root.xpath('//h1[@class="title title_level_1"]')[0].text_content()+" / "+root.xpath('//h2[@class="title title_level_2 location-title__place"]')[0].text_content()
    # p(headers)
    dyl = []
    for dy in root.xpath('//div[@class="content"]/div/dt'):        
        dyl.append(dy.xpath('strong')[0].text_content()+" "+dy.xpath('small/span')[0].text_content()+" "+dy.xpath('small/span')[1].text_content())
    # p(dyl, len(dyl))

    th = []
    for div in root.xpath('//div[@class="content"]/div/dd/table[@class="weather-table"]/thead')[0].xpath('th/div'):
        th.append(div.text_content())
    # p(th,len(th))

    wl = []
    for i,tr in enumerate(root.xpath('//div[@class="content"]/div/dd/table[@class="weather-table"]/tbody[@class="weather-table__body"]')):
        trl = []
        # trl.append([dyl[i],'',th[0],th[1],th[2],th[3]])
        trl.append([dyl[i],'','','','',''])
        for td in tr.xpath('tr'):
            tdl = []
            tdl.append(td.xpath('td')[0].xpath('div/div')[0].text_content()+" "+td.xpath('td')[0].xpath('div/div')[1].text_content())
            # tdl.append(repleces(td.xpath('td')[1].xpath('i')[0].attrib["class"], ['icon ',' icon_color_dark']))
            tdl.append(td.xpath('td')[2].text_content())
            tdl.append(td.xpath('td')[3].text_content())
            tdl.append(td.xpath('td')[4].text_content())
            tdl.append(isTrue(td.xpath('td')[5]))
            tdl.append(td.xpath('td')[6].text_content())            
            ###
            trl.append(tdl)
        wl.append(trl)
        
    # p(wl, len(wl))           

    return {'TITLE':headers,'HEADER':th,'ITEMS':wl}


def main():    
    url = {
            'moscow':'https://yandex.ru/pogoda/moscow/details',
            'petersburg':'https://yandex.ru/pogoda/saint-petersburg/details',
            'yekaterinburg':'https://yandex.ru/pogoda/yekaterinburg/details',
            'novosibirsk':'https://yandex.ru/pogoda/novosibirsk/details',
            'kaliningrad':'https://yandex.ru/pogoda/kaliningrad/details',
            'krasnoyarsk':'https://yandex.ru/pogoda/krasnoyarsk/details',
            'kazan':'https://yandex.ru/pogoda/kazan/details',
            'ufa':'https://yandex.ru/pogoda/ufa/details',
            'chelyabinsk':'https://yandex.ru/pogoda/chelyabinsk/details',
        }
    weather = parseHTML(get_html(url['kaliningrad']))
    if weather:
        with open('weather.txt', 'w', encoding='utf-8') as f:
            json.dump(weather, f)
    else:
        with open('weather.txt', 'r', encoding='utf-8') as f:
            weather = json.load(f)
    # p(weather)
    ###
    root = tk.Tk()
    root.title(weather['TITLE'])
    th = weather['HEADER']
    table = Table(root,['Время','Описание',th[0],th[1],th[2],th[3]],weather['ITEMS'])
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()


if __name__ == '__main__':
    main()