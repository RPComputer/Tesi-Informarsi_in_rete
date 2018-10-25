import mysql.connector
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import nltk


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
	insertconnection = connect_to_db()
	insertcursor = insertconnection.cursor()
	for t in topics:
		if t in tlist:
			#Inserimento della correlazione nel database
			correlation_query = ("INSERT INTO articolitopic (articolo, topic) VALUES (%s, %s)")
			correlation_data = (article[0], t)
			insertcursor.execute(correlation_query, correlation_data)
		else:
			#Inserimento dei dati nel database
			tlist.append(t)
			ltopic = ltopic + 1
			
			extracted_topic = ("INSERT INTO topic (nome) VALUES (%s)")
			extracted_data = (t)
			insertcursor.execute(extracted_topic, extracted_data)
			
			correlation_query = ("INSERT INTO articolitopic (articolo, topic) VALUES (%s, %s)")
			correlation_data = (article[0], t)
			insertcursor.execute(correlation_query, correlation_data)
	sentiment_query = ("UPDATE articoli SET sentiment WHERE link VALUES (%s, %s)")
	sentiment_data = (sent[1], article[0])
	insertcursor.execute(sentiment_query, sentiment_data)
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

articlecursor.execute("SELECT COUNT * FROM articoli")
n_articoli_tot = articlecursor.fetchall()
articlecursor.execute("SELECT COUNT * FROM articoli WHERE empytext = 0")
n_articoli = articlecursor.fetchall()
n_articoli_empty = n_articoli_tot - n_articoli
progress = 0

print("Statistiche articoli:")
print("Articoli: ", n_articoli_tot)
print("Articoli analizzabili: ", n_articoli)
print("Articoli non analizzabili: ", n_articoli_empty)

print("Raccolta articoli...\n")
articlecursor.execute("SELECT * FROM articoli WHERE empytext = 0")
articoli = articlecursor.fetchall()

print("Articoli ottenuti\n")

#ottenere lista topic
#articlecursor.execute("SELECT * FROM topic")
#tlist = articlecursor.fetchall()
tlist = []
ltopic = 0

articlecursor.close()
articleconnection.close()

print("Analisi articoli - Individuazione topic in corso...\n")

for a in articoli:
	text = TextBlob(a[1], analyzer=NaiveBayesAnalyzer())
	if text.detect_language() == "it":
		#poichè in italiano la ricerca dei nomi funziona molto peggio rispetto all'inglese effettuo la traduzione, il risultato più affidabile
		text = text.translate(to="en")
	
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
		for a in atmp:
			if contains_word(a, t):
				f = False
		if f:
			topic.append(t)
	
	insert_topics(topic, a, s)
		
	#Output di aggiornamento
	progress = progress + 1
	percentage = progress/n_articoli*100
	print("Avanzamento: ", percentage, "%   ", progress, "/", n_articoli, " - Topic individuati: ", ltopic, end='\r')
	



#chiusura script

print("\n---------- ESECUZIONE TERMINATA! ----------")