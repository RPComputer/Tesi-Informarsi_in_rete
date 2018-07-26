import mysql.connector
import feedparser
import urllib2
from datetime import datetime

'''
Collegarsi al database
Ottenere la lista dei siti
Collegarsi ai siti web e scaricare le notizie
Per ogni notizia scaricata eseguire le operazioni di salvataggio
Per ogni operazione completata dare output per seguire il programma
'''

#connessione al database
print("MODULO 1 - ESECUZIONE\n")
print("Connessione al database... ")

try:
dbconnection = mysql.connector.connect(user='module1', password='insertnews', host='localhost', database='tesi')
except mysql.connector.Error as err:
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
elencositi = dbcursor.execute("SELECT * FROM linkfeed")
print("Elenco siti ottenuto\n")

#for ogni link nel feed connettiti e salva l'html
print("Raccolta notizie:\n")
for s in elencositi:
	print("Connessione a: " + s.link + "\n")
	#ottenere elenco link notizie già scaricate
	elenconotizie = dbcursor.execute("SELECT dlink FROM notizie")
	r = feedparser.parse(s.link)
	for i in r.entries:
		errorFlag = 0
		l = i.link
		#se la notizia è già stata scaricata non si fa niente, altrimenti si scarica e inserisce nel database
		if l not in elenconotizie:
			try:
			response = urllib2.urlopen(l)
			except urllib2.HTTPError, e:
				logerror = ("INSERT INTO log (sito, downloadsuccess, info) VALUES (%s, %s, %s)")
				errordata = (s.sitoweb, 0, e.reason)
				dbcursor.execute(logerror, errordata)
				dbconnection.commit()
				errorFlag = 1
			if errorFlag == 0:
				html = response.read()
				#inserire nel database il codice html
				inserimento = ("INSERT INTO notizie (dlink, data, sitoweb, notizia) VALUES (%s, %s, %s, %s)")
				dati = (l, datetime.strptime(i.published[:-4], '%a, %d %b %Y %H:%M:%S').isoformat(), s.sitoweb, html)
				log = ("INSERT INTO log (sito, downloadsuccess, notizia) VALUES (%s, %s, %s)")
				datalog = (s.sitoweb, 1, l)
				dbcursor.execute(inserimento, dati)
				dbcursor.execute(log, datalog)
				dbconnection.commit()
				print("Download notizia completato...\n")
			else print("Errore di connessione al sito!\n")
		else print("Notizia gia' scaricata\n")




#chiusura script
dbcursor.close()
dbconnection.close()