import mysql.connector
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import nltk
import time


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

def insert_topics(topics, article, sent):
	global ltopic
	global t3, t4
	insertconnection = connect_to_db()
	insertcursor = insertconnection.cursor()
	for t in topics:
		t3 = time()
		if (t,) in tlist:
			t4 = time() - t3
			#Inserimento della correlazione nel database
			correlation_query = ("INSERT INTO articolitopic (articolo, topic) VALUES (%s, %s)")
			correlation_data = (article[0], t)
			try:
				insertcursor.execute(correlation_query, correlation_data)
			except mysql.connector.Error as e:
				print("\nErrore durante inserimento correlazione")
				print(e)
		else:
			t4 = time() - t3
			#Inserimento dei dati nel database
			tlist.add((t,))
			ltopic = ltopic + 1
			
			extracted_topic = ("INSERT INTO topic (nome) VALUES (%s)")
			extracted_data = (t,)
			try:
				insertcursor.execute(extracted_topic, extracted_data)
			except mysql.connector.Error as e:
				print("\nErrore durante inserimento topic")
				print(e)
			
			correlation_query = ("INSERT INTO articolitopic (articolo, topic) VALUES (%s, %s)")
			correlation_data = (article[0], t)
			try:
				insertcursor.execute(correlation_query, correlation_data)
			except mysql.connector.Error as e:
				print("\nErrore durante inserimento correlazione")
				print(e)
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

#connessione al database
print("---------- MODULO 2 - ESECUZIONE ----------\n")
print("------- Elaborazione topic articoli--------\n")
print("Connessione al database... ")
articleconnection = connect_to_db()
articlecursor = articleconnection.cursor();
print("completata\n")

articlecursor.execute("SELECT COUNT(*) FROM articoli")
(n_articoli_tot,) = articlecursor.fetchone()
articlecursor.execute("SELECT COUNT(*) FROM articoli WHERE emptytext = 0")
(n_articoli,) = articlecursor.fetchone()
n_articoli_empty = n_articoli_tot - n_articoli
articlecursor.execute("SELECT COUNT(DISTINCT articolo) FROM articolitopic")
(progress,) = articlecursor.fetchone()

print("Statistiche articoli:")
print("Articoli: ", n_articoli_tot)
print("Articoli analizzabili: ", n_articoli)
print("Articoli non analizzabili: ", n_articoli_empty)

#ottenere lista topic
articlecursor.execute("SELECT * FROM topic")
tlist = set(articlecursor.fetchall())

print("Raccolta articoli...\n")
articlecursor.execute("SELECT * FROM articoli WHERE emptytext = 0 AND link NOT IN (SELECT DISTINCT articolo FROM articolitopic)")


print("Articoli ottenuti\n")


#tlist = []
ltopic = len(tlist)

t3
t4

print("Analisi articoli - Individuazione topic in corso...\n")

while True:
	articoli = articlecursor.fetchmany(3000)
	if articoli == ():
		break
	for a in articoli:
		text = TextBlob(a[1], analyzer=NaiveBayesAnalyzer())
		t0 = time()
		if text.detect_language() == "it":
			#poichè in italiano la ricerca dei nomi funziona molto peggio rispetto all'inglese effettuo la traduzione, il risultato più affidabile
			text = text.translate(to="en")
		t1 = time() - t0
		s = text.sentiment
		
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
			
		#Output di aggiornamento
		progress = progress + 1
		percentage = progress/n_articoli*100
		print("Avanzamento: %0.3f" % percentage, "% \t", progress, "/", n_articoli, "\t - Topic individuati: ", ltopic, "Tempo traduzione: ", t1, "  Tempo controllo: ", t4, end='\r')
	
articlecursor.close()
articleconnection.close()


#chiusura script

print("\n---------- ESECUZIONE TERMINATA! ----------")