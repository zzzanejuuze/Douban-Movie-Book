import numpy as np
import urllib.request, urllib.parse, urllib.error
import time
import ssl
from openpyxl import Workbook
from bs4 import BeautifulSoup

# Some user agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

context = ssl._create_unverified_context()

def book_spider(book_tag):
	page_num = 0
	book_list = []
	try_times = 0
	
	while(1):
	# https://www.douban.com/tag/%E5%B0%8F%E8%AF%B4/book?start=0
		url = 'https://www.douban.com/tag/' + urllib.parse.quote(book_tag) + '/book?start=' + str(page_num*15)
		time.sleep(np.random.rand()*5)

		try:
			req = urllib.request.Request(url, headers=hds[page_num % len(hds)])   # 设置headers信息 模拟浏览器去访问网址
			source_code = urllib.request.urlopen(req, context=context).read()
		except (urllib.error.HTTPError):
			print('There is an error')
			continue

		soup = BeautifulSoup(source_code, 'html.parser')
		list_soup = soup.find('div', {'class' : 'mod book-list'})

		try_times+=1
		if list_soup == None and try_times < 200:
			continue
		elif list_soup == None or len(list_soup) <= 1:
			break 											# Break when no information after 200 times requesting

		for book_info in list_soup.findAll('dd'):
			title = book_info.find('a', {'class' : 'title'}).string.strip()
			desc = book_info.find('div', {'class':'desc'}).string.strip()
			author = desc.split('/')[0]
			book_url = book_info.find('a', {'class':'title'}).get('href')
			
			try:
				rating = book_info.find('span', {'class':'rating_nums'}).string.strip()
			except:
				rating = '0.0'
			
			people_nums = get_people_num(book_url)

			book_list.append([title, author, book_url, rating, people_nums])
			try_times = 0
		page_num+=1
		print('Downloading information from page %s' % page_num)
	return book_list


def get_people_num(url):
	# https://book.douban.com/subject/1770782/?from=tag_all
	
	req = urllib.request.Request(url, headers=hds[np.random.randint(0, len(hds))])
	source_code = urllib.request.urlopen(req, context=context).read()
	soup = BeautifulSoup(source_code, 'html.parser')

	try:
		people_nums = soup.find('span', {'property':'v:votes'}).string.strip()
	except:
		people_nums = '0'

	return people_nums

def book_list_excel(book_list, book_tag):
	wb = Workbook()
	ws = wb.create_sheet(title=book_tag)
	ws.append(['书名', '作者', '网址', '评分', '评论人数'])

	for row in book_list:
		ws.append(row)

	wb.save('test.xlsx')



book_tag = '小说'
book_lists = book_spider(book_tag)
print(book_list_excel(book_lists, book_tag))



		


















