# парсинг расписания фильмов
import sys
import requests
import json # сохраняем все в json
from lxml import html  # для xml для html нужно -- from lxml import html
# import re, cgi
import tkinter as tk
import tkinter.ttk as ttk

class Table(tk.Frame):
    def __init__(self, parent=None, headings=list(), rows=list()):
        tk.Frame.__init__(self, parent)
        #
        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table.tag_configure('STYLE_DATE', background='#777777', font=("Verdana", 8, 'bold'), foreground="#fff")
        table.tag_configure('STYLE_TITLE', background='#e1e1e1', font=("Verdana", 8, 'bold'))
        #
        table["columns"] = headings
        table["displaycolumns"] = headings        
        # формируем заголовок таблицы
        for h,head in enumerate(headings):
            #print (head)
            anchor = 'c' if head == 'ID' or head == 'Name' else 'w'
            width = 400 if h == 2 else 300
            table.heading(head, text=head, anchor='c')
            table.column(head, width=width, anchor=anchor)            
        # формируем значение в cтроках      
        for i,row in enumerate(rows):
            # p(row)
            table.insert('', 'end', text='L'+str(i), values=list(row[1]), tags=(row[0]))

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

def getFilmList(sc):
	# scl = []
	cinema = sc.xpath('dt[@class="name"]')[0].text_content()	
	tm = []
	for time in sc.xpath('dd[@class="time"]')[0].xpath('i|u|b'):
		time = time.text_content().replace(' ','').replace('\n','')
		tm.append(time)
	return [cinema,tm]

def getFilmTime(fm):
	fmn = str(fm.xpath('div[@class="title _FILM_"]/div/p/a')[0].text_content())
	# +18, +12, +6
	age = fm.xpath('div[@class="title _FILM_"]/div/p/span')[0].attrib["class"] if fm.xpath('div[@class="title _FILM_"]/div/p/span') else False
	age = "+"+str(age.split()[2].replace('age','')) if age else False
	# Name films abd age
	fmn = str(fmn+" "+age) if age else fmn
	# p(fmn)
	fmInfo = [ f.text_content() for f in fm.xpath('div[@class="title _FILM_"]/ul/li') ]
	# p(fmInfo)
	fmList = [ getFilmList(sc) for sc in fm.xpath('div[@class="showing_section"]/dl') ]
	# p(fmList)
	return {'F_TITLE':fmn,'F_INFO':fmInfo,'F_TIME':fmList}

def get_html(url):
	try:
		page = requests.get(url)
		return page.text
	except Exception: # requests.exceptions.ConnectionError: # Exception:		
		# вызов кода ошибки
		print(sys.exc_info()[1])
		return False

def parseHTML(html_content):
	# Парсинг HTML
	if html_content == False:
		return False
	#print (html_content)
	root = html.fromstring(html_content)
	# print(root.attrib["class"])
	body = root.xpath('//td[@id="block_left"]/div[@class="block_left"]/table/tr/td')
	headers = body[0].xpath('table/tr/td[@colspan="3"]')[0].xpath('table/tr/td[@colspan="3"]/a')[0].text_content()
	# p(headers);
	KP = []	# куда сохраняем все данные с парсинга
	dtFilm = body[0].xpath('div[@class="showing"]')
	for dt in dtFilm:    	
		showDate = dt.xpath('div[@class="showDate"]|div[@class="showDate gray"]')[0].text_content()
		# p(showDate)  
		FL = [ getFilmTime(fm) for fm in dt.xpath('div[@class="films_metro "]|div[@class="films_metro"]') ]  	
		# p(FL)
		KP.append({'F_DATE':showDate,'F_SCHEDULE':FL})
	return {'TITLE':headers,'ITEMS':KP}

def main():
	url = 'https://www.kinopoisk.ru/afisha/city/490/'
	kino = parseHTML(get_html(url))
	if kino:
		with open('kino.txt', 'w', encoding='utf-8') as f:
			json.dump(kino, f)
	else:
		with open('kino.txt', 'r', encoding='utf-8') as f:
			kino = json.load(f)
	# p(kino['ITEMS'])
	rows = []
	for items in kino['ITEMS']:
		rows.append(['STYLE_DATE',[items['F_DATE'],'']])
		for schedules in items['F_SCHEDULE']:
			# p(schedules)
			rows.append(['STYLE_TITLE',[schedules['F_TITLE']," ".join(schedules['F_INFO'])]])
			for ft_ in schedules['F_TIME']:
				# p(ft_[0])
				# p(" ".join(ft_[1]))
				rows.append(['STYLE_TIME',[ft_[0]," ".join(ft_[1])]])
	###
	root = tk.Tk()
	root.title(kino['TITLE'])
	table = Table(root,['ДАТА / ФИЛЬМ / МЕСТО','ОПИСАНИЕ / ВРЕМЯ'],rows)
	table.pack(expand=tk.YES, fill=tk.BOTH)
	root.mainloop()


if __name__ == '__main__':
	main()