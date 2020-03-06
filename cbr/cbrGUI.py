# currency parsing http://www.cbr.ru/scripts/XML_daily.asp
import requests
from lxml import etree # from xml and html necessary -- from lxml import html
import PySimpleGUI as sg
import sys
import json

def p(text, *args):
    print(text, *args, sep = ' / ', end = '\n')

def get_html(url):
    try:
        page = requests.get(url)
        return page.content
    except requests.exceptions.ConnectionError:
        print('Seems like dns lookup failed..')
        return False

def parseXML(xml_content):
    # parsing XML
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
    #p(cur)
    headings = []
    for key in cur['ITEMS'][0].keys():
        headings.append(key)
    #p(headings)
    rows = []
    for item in cur['ITEMS']:
        row = []
        for rw in item.values():
            row.append(rw)
        rows.append(row)
    # ------ the table ------
    favicon = "favicon.ico" # the icon from windows
    sg.theme('Dark')
    # ------ Window Layout ------
    layout = [[sg.Table(values=rows, headings=headings, max_col_width=25,
                # background_color='light blue',
                auto_size_columns=True,
                display_row_numbers=False,
                justification='left',
                num_rows=20,                 
                #alternating_row_color='lightyellow',
                enable_events=True,
                key='-TABLE-',
                tooltip=('This is a table').upper())]]
    # ------ Create Window ------
    window = sg.Window(('Exchange rates on ').upper() + cur['DATE'], layout, icon = favicon)
    while True:
        event, values = window.read()
        if event in (None, '_cansel_'):   # if user closes window or clicks cancel
            break
        if event == '-TABLE-':
            p(rows[values['-TABLE-'][0]])

    window.close()

if __name__ == '__main__':
    main()