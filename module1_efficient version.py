import mysql.connector
import feedparser
import urllib
import urllib.request
from urllib.request import urlopen
from urllib.request import Request
from datetime import datetime
import sys
import threading

'''
Collegarsi al database
Ottenere la lista dei siti
Collegarsi ai siti web e scaricare le notizie
Per ogni notizia scaricata eseguire le operazioni di salvataggio
Per ogni operazione completata dare output per seguire il programma
'''

def connect_to_db():
	try:
		res = mysql.connector.connect(user='module1', password='insertnews', host='localhost', database='tesi')
		return res
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("\nPassword e/o username errati")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("\nDatabase does not exist")
		else:
			print("\nErrore: " + err)
		return None

		
#Classe Threads per il download delle notizie
class newsDownloader (threading.Thread):
	def __init__(self, site):
		threading.Thread.__init__(self)
		self.s = site
	def run(self):
		print("Avvio thread: ", s[0])
		dbconnection = connect_to_db()
		dbcursor = dbconnection.cursor();
		#ottenere elenco link notizie già scaricate
		dbcursor.execute("SELECT dlink FROM notizie")
		elenconotizie = dbcursor.fetchall()
		dbcursor.execute("SELECT notizia, linkfeed FROM notizielinkfeed")
		elencocorrelazioni = dbcursor.fetchall()
		r = feedparser.parse(s[0])
		print("parsed")
		for i in r.entries:
			errorFlag = 0
			if hasattr(i, 'link'):
				l = i.link
				notinsertedflag = 0
				#se la notizia è già stata scaricata non si fa niente, altrimenti si scarica e inserisce nel database
				if (l,) not in elenconotizie and len(l) > 0:
					try:
						req = Request(l)
						req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
						response = urlopen(req)
						html = response.read()
					except:
						e = sys.exc_info()[0]
						logerror = ("INSERT INTO log (sito, downloadsuccess, info) VALUES (%s, %s, %s)")
						errordata = (s[1], 0, str(e))
						dbcursor.execute(logerror, errordata)
						dbconnection.commit()
						errorFlag = 1
					if errorFlag == 0:
						elenconotizie.append((l,))
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
						correlazione = ("INSERT INTO notizielinkfeed (notizia, linkfeed) VALUES (%s, %s)")
						correlazione_data = (l, s[0])
						try:
							dbcursor.execute(inserimento, dati)
						except mysql.connector.Error as e:
							notinsertedflag = notinsertedflag + 1
							print("\nErrore durante inserimento codice html")
							print(e)
						try:
							dbcursor.execute(correlazione, correlazione_data)
						except mysql.connector.Error as e:
							notinsertedflag = notinsertedflag + 1
							print("\nErrore durante inserimento correlazione")
							print(e)
						try:
							dbcursor.execute(log, datalog)
						except mysql.connector.Error as e:
							notinsertedflag = notinsertedflag + 1
							print("Errore durante inserimento log")
							print(e)
						try:
							dbconnection.commit()
						except mysql.connector.Error as e:
							notinsertedflag = notinsertedflag + 1
							print("Errore durante commit")
							print(e)
						if notinsertedflag == 0:
							print("↓", end ="", flush=True)
					else:
						print("\nErrore download in: ", s[0])
				else:
					if (l,s[0]) not in elencocorrelazioni:
						correlazione = ("INSERT INTO notizielinkfeed (notizia, linkfeed) VALUES (%s, %s)")
						correlazione_data = (l, s[0])
						try:
							dbcursor.execute(correlazione, correlazione_data)
						except mysql.connector.Error as e:
							notinsertedflag = notinsertedflag + 1
							print("\nErrore durante inserimento correlazione")
							print(e)
					print("→", end ="", flush=True)
			else:
				log = ("INSERT INTO log (sito, downloadsuccess, notizia, info) VALUES (%s, %s, %s, %s)")
				datalog = (s[1], 0, None, "attributo link non presente")
				try:
					dbcursor.execute(log, datalog)
				except mysql.connector.Error as e:
					print("Errore durante inserimento log")
					print(e)
		dbcursor.close()
		dbconnection.close()
		print("\nThread", s[0], " terminato\n")

		
		
#connessione al database
print("---------- MODULO 1 - ESECUZIONE ----------\n")
print("Connessione al database... ")

dbconnection = connect_to_db()

print("completata\n")

#raccolta link siti web
print("Raccolta link siti web...\n")
dbcursor = dbconnection.cursor();
dbcursor.execute("SELECT * FROM linkfeed")
elencositi = dbcursor.fetchall()
print("Elenco siti ottenuto\n")
dbcursor.close()
dbconnection.close()

#for ogni link nel feed connettiti e salva l'html
#necessario lanciare un numero limitato di thread, circa 5 per volta
print("Raccolta notizie - avvio dei thread:\n")
threads = []
count = 0
for s in elencositi:
	thread = newsDownloader(s)
	thread.start()
	threads.append(thread)
	count = count + 1
	if count >= 5:
		print("Avvio ciclo 5 thread")
		for t in threads:
			t.join()
		threads = []
		count = 0


print("---------- ESECUZIONE TERMINATA! ----------")