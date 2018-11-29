'''
Nome:
Controllo manuale dell'estrazione

Obiettivo:
L'algoritmo estrae il testo e il titolo di una notizia e li stampa a schermo

Passaggi:
Richiesta del sito da cui estrarre la notizia
Scaricamento della notizia
Estrazione della notizia
Stampa a schermo del titolo e della notizia
'''


import os
from newspaper import Article


#Inizio script

while True:
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

#Fine Script