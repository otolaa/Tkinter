# парсинг coinmarketcap.com
import sys
import requests, fake_useragent  # pip install requests
import json
import csv
from datetime import datetime
# from multiprocessing import Pool
from bs4 import BeautifulSoup
# Теперь для Python 3.6 есть beautifulsoup4.

def p(text, *args):		# вспомогательная функция для быстрого вывода на экран данных
	print(text, *args, sep=' / ', end='\n')

def get_html(url):
	# Random User-Agent
	ua = fake_useragent.UserAgent() 
	user = ua.random
	header = {'User-Agent':str(user)}
	try:
		page = requests.get(url, headers = header, timeout = 10)
		return page.text		# возвращает html код станицы (url)
	except Exception as e:
		print(sys.exc_info()[1])
		return False

def get_all_links(html):
	soup = BeautifulSoup(html, 'lxml')
	tds = soup.find('table',id='currencies-all').find_all('td',class_='currency-name')
	links = []
	for td in tds:
		a = td.find('a').get('href')
		name = td.find('a',class_='currency-name-container').text.strip()
		symbol = td.find('span',class_='currency-symbol').text.strip()
		link = 'https://coinmarketcap.com' + a
		row = []
		row.append(link)
		row.append(name)
		row.append(symbol)
		links.append(row)
	return links

def get_page_data(html):
	soup = BeautifulSoup(html, 'lxml')
	try:
		name = soup.find('h1',class_='details-panel-item--name').text.strip()
	except:
		name = ''
	try:
		prise = soup.find('span',id='quote_price').text.strip()
	except:
		prise = ''

	data = {'name':name,'prise':prise}
	return data

def csv_reader():
	arr_reader = []
	with open('coinmarketcap.csv', 'r') as f:
		reader = csv.reader(f)
		# p(reader)
		for row in reader:
			# p(row)
			arr_reader.append(row)
			# p(" ".join(row))
	return arr_reader

def write_csv(data):
	with open('coinmarketcap.csv','a') as f:
		writer = csv.writer(f)
		writer.writerow((data))

def main():
	start = datetime.now()
	url = 'https://coinmarketcap.com/all/views/all/'	
	all_links = get_all_links(get_html(url))
	# p(all_links)
	p(len(all_links))

	coin = []
	for index, data in enumerate(all_links):
		# p(data)
		write_csv(data)
	# --- reader in files
	arr_reader = csv_reader()
	p(arr_reader)


	end = datetime.now()
	print(str(end-start))


if __name__ == '__main__':
	main()