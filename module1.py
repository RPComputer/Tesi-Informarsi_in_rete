import pymysql
import feedparser
import urllib
from urllib.request import urlopen
from datetime import datetime

'''
Collegarsi al database
Ottenere la lista dei siti
Collegarsi ai siti web e scaricare le notizie
Per ogni notizia scaricata eseguire le operazioni di salvataggio
Per ogni operazione completata dare output per seguire il programma
'''

#connessione al database
print("---------- MODULO 1 - ESECUZIONE ----------\n")
print("Connessione al database... ")

try:
	dbconnection = pymysql.connect(user='module1', password='insertnews', host='localhost', database='tesi')
except pymysql.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("\nPassword e/o username errati")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("\nDatabase does not exist")
	else:
		print("\nErrore: " + err)

print("completata\n")

#raccolta link siti web
print("Raccolta link siti web...\n")
dbcursor = dbconnection.cursor();
dbcursor.execute("SELECT * FROM linkfeed")
elencositi = dbcursor.fetchall()
print("Elenco siti ottenuto\n")

#for ogni link nel feed connettiti e salva l'html
print("Raccolta notizie:\n")
for s in elencositi:
	print("Connessione a: " + s[0] + "\n")
	#ottenere elenco link notizie già scaricate
	dbcursor.execute("SELECT dlink FROM notizie")
	elenconotizie = dbcursor.fetchall()
	r = feedparser.parse(s[0])
	for i in r.entries:
		errorFlag = 0
		l = i.link
		#se la notizia è già stata scaricata non si fa niente, altrimenti si scarica e inserisce nel database
		if (l,) not in elenconotizie:
			try:
				response = urlopen(l)
			except urllib.error.HTTPError as e:
				logerror = ("INSERT INTO log (sito, downloadsuccess, info) VALUES (%s, %s, %s)")
				errordata = (s[1], 0, e.reason)
				dbcursor.execute(logerror, errordata)
				dbconnection.commit()
				errorFlag = 1
			if errorFlag == 0:
				elenconotizie.append((l,))
				html = response.read()
				#inserire nel database il codice html
				inserimento = ("INSERT INTO notizie (dlink, data, sitoweb, notizia) VALUES (%s, %s, %s, %s)")
				if hasattr(i, 'published'):
					try:
						datanotizia = datetime.strptime(i.published[0:25], '%a, %d %b %Y %H:%M:%S').isoformat()
					except ValueError:
						datanotizia = None
				else: datanotizia = None
				dati = (l, datanotizia, s[1], html)
				log = ("INSERT INTO log (sito, downloadsuccess, notizia) VALUES (%s, %s, %s)")
				datalog = (s[1], 1, l)
				try:
					dbcursor.execute(inserimento, dati)
				except mysql.connector.Error as e:
					print(e)
				try:
					dbcursor.execute(log, datalog)
				except mysql.connector.Error as e:
					print(e)
				dbconnection.commit()
				print("Download notizia completato...\n")
			else:
				print("Errore di connessione al sito!\n")
		else:
			print("Notizia gia' scaricata\n")




#chiusura script
dbcursor.close()
dbconnection.close()

print("---------- ESECUZIONE TERMINATA! ----------")