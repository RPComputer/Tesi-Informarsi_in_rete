import os
from newspaper import Article
while 1 < 2:
	lk = input('link: ')
	a = Article(lk)
	a.download()
	a.parse()
	print('\nTEXT:\n')
	print(a.text)
	print('\n\nTITLE:\n')
	print(a.title)
	print('\n\n')
	os.system("PAUSE")
	os.system("cls")