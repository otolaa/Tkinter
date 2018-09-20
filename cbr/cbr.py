# парсинг валюты http://www.cbr.ru/scripts/XML_daily.asp
import requests
import pickle
from lxml import etree # для xml для html нужно -- from lxml import html
# tkinter && treeview для формирования таблицы
import tkinter as tk
import tkinter.ttk as ttk

class Table(tk.Frame):
    def __init__(self, parent=None, headings=list(), rows=list()):
        tk.Frame.__init__(self, parent)
        #
        table = ttk.Treeview(self, show="headings", selectmode="browse")
        #
        table["columns"] = headings
        table["displaycolumns"] = headings
        # формируем заголовок таблицы
        for head in headings:
            #print (head)
            anchor = 'w' if head == 'ID' or head == 'Name' else 'c'
            width = 50 if head == 'ID' else 100
            if head == 'Name':
                width = 150
            table.heading(head, text=head, anchor='c')
            table.column(head, width=width, anchor=anchor)
        # формируем значение в cтроках
        i = 0
        for row in rows:
            table.insert('', 'end', text='L'+str(i), values=list(row))
            i+=1

        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)

def get_html(url):
    try:
        page = requests.get(url)
        return page.content
    except requests.exceptions.ConnectionError:
        print('Seems like dns lookup failed..')
        return False

def parseXML(xml_content):
    # Парсинг XML
    if xml_content == False:
        return False
    root = etree.fromstring(xml_content)
    #print(root.attrib["Date"])
    ValCurrency = []
    for appt in root.getchildren():
        #print(appt.attrib["ID"])
        currency = {}
        currency['ID'] = appt.attrib["ID"]
        for elem in appt.getchildren():
            text = False if not elem.text else elem.text
            #print (elem.tag + " => " + text)
            if elem.tag == "Value":
                text = float(text.replace(',', '.'))
            currency[elem.tag] = text
        #print (currency)
        ValCurrency.append(currency)
    return {'DATE':root.attrib["Date"],'ITEMS':ValCurrency}


def main():
    url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    cur = parseXML(get_html(url))
    if cur:
        with open('cbr.pickle', 'wb') as f:
            pickle.dump(cur, f)
    else:
        with open('cbr.pickle', 'rb') as f:
            cur = pickle.load(f)
    #print (cur['DATE'])
    headings = []
    for key in cur['ITEMS'][0].keys():
        headings.append(key)
    #print (headings)
    rows = []
    for item in cur['ITEMS']:
        row = []
        for rw in item.values():
            row.append(rw)
        rows.append(row)
    ###
    root = tk.Tk()
    root.title('КУРС ВАЛЮТ CBR.RU НА '+ cur['DATE'])
    table = Table(root,headings,rows)
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()

if __name__ == '__main__':
    main()