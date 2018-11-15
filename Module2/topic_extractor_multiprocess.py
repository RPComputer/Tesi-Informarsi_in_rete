import mysql.connector
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import nltk
from time import time
import multiprocessing


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

def contains_word(s, w):
	return(' ' + w + ' ') in (' ' + s + ' ')

def init(p, a):
	global progress
	global n_articoli
	progress = p
	n_articoli = a

def insert_topics(topics, article, sent):
	global ltopic
	#global t3, t4
	#t3 = time()
	insertconnection = connect_to_db()
	insertcursor = insertconnection.cursor()
	for t in topics:
		'''
		if (t,) in tlist:
			#Inserimento della correlazione nel database
			correlation_query = ("INSERT INTO articolitopic (articolo, topic) VALUES (%s, %s)")
			correlation_data = (article[0], t)
			try:
				insertcursor.execute(correlation_query, correlation_data)
			except mysql.connector.Error as e:
				#print("\nErrore durante inserimento correlazione")
				#print(e)
				pass
		else:
		'''
		#Inserimento dei dati nel database
		#tlist.add((t,))
		with ltopic.get_lock():
			ltopic.value += 1
		
		extracted_topic = ("INSERT INTO topic (nome) VALUES (%s)")
		extracted_data = (t,)
		try:
			insertcursor.execute(extracted_topic, extracted_data)
		except mysql.connector.Error as e:
			#print("\nErrore durante inserimento topic")
			#print(e)
			with ltopic.get_lock():
				ltopic.value -= 1
		
		correlation_query = ("INSERT INTO articolitopic (articolo, topic) VALUES (%s, %s)")
		correlation_data = (article[0], t)
		try:
			insertcursor.execute(correlation_query, correlation_data)
		except mysql.connector.Error as e:
			#print("\nErrore durante inserimento correlazione")
			#print(e)
			pass
	sentiment_query = ("UPDATE articoli SET sentiment = %s WHERE link = %s")
	sentiment_data = (sent[1], article[0])
	try:
		insertcursor.execute(sentiment_query, sentiment_data)
	except mysql.connector.Error as e:
		print("\nErrore durante inserimento sentiment")
		print(e)
	insertconnection.commit()
	insertcursor.close()
	insertconnection.close()
	#t4 = time() - t3


def article_handler(a):
	#t0 = time()
	text = TextBlob(a[1], analyzer=NaiveBayesAnalyzer())
	gt_flag = False
	while gt_flag == False:
		try:
			if text.detect_language() == "it":
				#poichè in italiano la ricerca dei nomi funziona molto peggio rispetto all'inglese effettuo la traduzione, il risultato più affidabile
				text = text.translate(to="en")
				gt_flag = True
		except:
			time.sleep(2)
	
	s = text.sentiment
	#t1 = time() - t0
	raw = text.noun_phrases
	#rimozione duplicati puri
	unique = list(set(raw))
	topic = []
	atmp = []
	#rimozione dei dublicati logici: es. sergio mattarella e mattarella sono la stessa cosa, viene mantenuto solo sergio mattarella
	for t in unique:
		f = True
		atmp = unique.copy()
		atmp.remove(t)
		for at in atmp:
			if contains_word(at, t):
				f = False
		if f:
			topic.append(str(t))
	
	insert_topics(topic, a, s)
	
	with progress.get_lock():
		progress.value += 1
	percentage = (progress.value/n_articoli.value)*100
	print("Avanzamento: %0.3f" % percentage, "% \t", progress.value, "/", n_articoli.value, "\t - Topic individuati: ", ltopic.value, end='\r')
	
#connessione al database
if __name__ == "__main__":
	print("---------- MODULO 2 - ESECUZIONE ----------\n")
	print("------- Elaborazione topic articoli--------\n")
	print("Connessione al database... ")
	articleconnection = connect_to_db()
	articlecursor = articleconnection.cursor();
	print("completata\n")

	n_articoli = multiprocessing.Value('i')
	articlecursor.execute("SELECT COUNT(*) FROM articoli")
	(n_articoli_tot,) = articlecursor.fetchone()
	articlecursor.execute("SELECT COUNT(*) FROM articoli WHERE emptytext = 0")
	(n_articoli.value,) = articlecursor.fetchone()
	n_articoli_empty = n_articoli_tot - n_articoli.value
	articlecursor.execute("SELECT COUNT(DISTINCT articolo) FROM articolitopic")
	(progressbase,) = articlecursor.fetchone()


	progress = multiprocessing.Value('i')
	with progress.get_lock():
		progress.value = progressbase

	print("Statistiche articoli:")
	print("Articoli: ", n_articoli_tot)
	print("Articoli analizzabili: ", n_articoli.value)
	print("Articoli non analizzabili: ", n_articoli_empty)

	#ottenere lista topic
	#articlecursor.execute("SELECT * FROM topic")
	#tlist = set(articlecursor.fetchall())
	ltopic = multiprocessing.Value('i')
	articlecursor.execute("SELECT COUNT(*) FROM topic")
	with ltopic.get_lock():
		(ltopic.value,) = articlecursor.fetchone()

	print("Raccolta articoli...\n")
	articlecursor.execute("SELECT * FROM articoli WHERE emptytext = 0 AND link NOT IN (SELECT DISTINCT articolo FROM articolitopic)")


	print("Articoli ottenuti\n")



	#t3 = 0
	#t4 = 0

	print("Analisi articoli - Individuazione topic in corso...\n")

	pool = multiprocessing.Pool(initializer  = init, initargs = (progress, n_articoli))


	while True:
		fetch_flag = False
		while fetch_flag == False:
			try:
				articoli = articlecursor.fetchmany(3000)
				fetch_flag = True
			except:
				fetch_flag = False
				print("Persa connessione al database, rilancio query")
			if fetch_flag == False:
				articleconnection = connect_to_db()
				articlecursor = articleconnection.cursor();
				articlecursor.execute("SELECT * FROM articoli WHERE emptytext = 0 AND link NOT IN (SELECT DISTINCT articolo FROM articolitopic)")
		if articoli == ():
			break
		
		pool.map_async(article_handler, articoli)
		#pool.join()
		
			
		
	articlecursor.close()
	articleconnection.close()


	#chiusura script

	print("\n---------- ESECUZIONE TERMINATA! ----------")