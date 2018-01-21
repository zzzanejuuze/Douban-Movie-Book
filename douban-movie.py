import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import ssl

context = ssl._create_unverified_context()

url = 'https://movie.douban.com/'
html = urllib.request.urlopen(url, context = context).read()
soup = BeautifulSoup(html, 'html.parser')

i = 0
tags = soup('li')
for tag in tags:
	title = tag.get('data-title')
	rate = tag.get('data-rate')
	
	if title is None:
		continue
	else:
		i = i + 1
		print(title,rate)

print('======================================')
print('一共有:',i,'部影片')
