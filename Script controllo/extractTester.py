import os
from newspaper import Article
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
#m = input('Enter to close: ')