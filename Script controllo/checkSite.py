'''
Nome:
Controllo dei siti

Obiettivo:
L'algoritmo controlla se un sito permette o meno il download

Passaggi:
Connessione al database
Raccolta della lista dei siti web
Richiesta di connessione
Stampa stato a schermo
'''


import urllib.request
import feedparser
from urllib.request import urlopen
from urllib.request import Request
import mysql.connector


#Inizio script

try:
	dbconnection = mysql.connector.connect(user='module1', password='insertnews', host='192.168.1.104', database='tesi')
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("\nPassword e/o username errati")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("\nDatabase does not exist")
	else:
		print("\nErrore: " + err)

#Caricamento dell'elenco dei siti
dbcursor = dbconnection.cursor();
dbcursor.execute("SELECT * FROM linkfeed")
elencositi = dbcursor.fetchall()

print("Controllo in corso...\n")

for s in elencositi:
	i=0
	try:
		r = feedparser.parse(s[0])
	except feedparser.error as e:
		print(s)
		print(e)
		i = 1
	if i == 0:
		y=0
		try:
			l = r.entries[0].link
		except IndexError as e:
			y = 1
			print(s)
			print(e)
		if y == 0:
			req = Request(l)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
			try:
				response = urlopen(req)
			except urllib.error.HTTPError as e:
				print(s)
				print(e)
			html = response.read()
			
print("Fine controllo\n\n")

#Fine script