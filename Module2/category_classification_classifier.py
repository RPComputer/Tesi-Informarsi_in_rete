'''
ALGORITMO NON FUNZIONANTE

Nome:
Classificatore degli articoli multi-processo

Obiettivo:
Classificare tutti gli articoli nelle categorie prescelte mediante il modello precedentemente preparato

Passaggi:
Collegarsi al database
Ottenere gli articoli
Effettuare la classificazione dell'insieme di articoli ottenuto
Salvare il risultato sul database
'''

import mysql.connector
from sklearn.externals import joblib
from time import time
import multiprocessing

#Funzione di connessione al database
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

#Funzione di inizializzazione per i sottoprocessi
def init(v, c, t, p, a):
	#Ottine le variabili globali dal processo principale
	global vectorizer
	global clf
	global t0
	global progress
	global articlenum
	vectorizer = v
	clf = c
	t0 = t
	progress = p
	articlenum = a

#Funzione che si occupa di classificare un articolo e salvarne la categoria nel database
def classifica(a):
	#Preparazione dei dati: trasformazione del testo in matrice numeriche per migliorare l'efficenza del codice mediante sempre il medesimo trasformatore
	testo = vectorizer.transform(a[1])
	#Classificazione del testo
	categoria = clf.predict(testo)
	#Salvataggio nel database della categoria
	insertconnection = connect_to_db()
	insertcursor = insertconnection.cursor()
	
	cat_query = ("UPDATE articoli SET categoria, ce_flag WHERE link VALUES (%s, %s, %s)")
	cat_data = (categoria, 1, a[0])
	insertcursor.execute(cat_query, cat_data)
	#Chiusura connessione
	insertconnection.commit()
	insertcursor.close()
	insertconnection.close()
	#Output di aggiornamento
	t = time() - t0.value
	with progress.get_lock():
		progress.value += 1
	percentage = progress.value/articlenum.value*100
	print("Avanzamento: ", percentage, "%   ", progress.value, "/", articlenum.value, "   -   Tempo trascorso: %0.3fs" % t, end='\r')

#Inizio script
#Gestione del processo principale
if __name__ == "__main__":
	print("--------------------------- MODULO 2 - ESECUZIONE ---------------------\n")
	print("---------- Elaborazione categorie articoli - Classificazione-----------\n")

	print("Connessione al database... ")
	dbconnection = connect_to_db()
	dbcursor = dbconnection.cursor();
	print("completata\n")
	
	#Caricamento ed inizializzazione delle variabili globali
	print("Raccolta articoli da classificare...\n")
	dbcursor.execute("SELECT link, testo FROM articoli WHERE emptytext = 0 AND categoria IS NULL")

	print("Caricamento classificatore")
	clf = joblib.load('category_classification_model.pkl')

	vectorizer = joblib.load('category_classification_vectorizer.pkl')

	progress = multiprocessing.Value('i')
	with progress.get_lock():
		progress.value = 0
	articlenum = multiprocessing.Value('i')
	with articlenum.get_lock():
		articlenum.value = 163008



	print("Avvio classificazione...")
	t0 = multiprocessing.Value('f')
	with t0.get_lock():
		t0.value = time()
	#Classificazione degli articoli, 5000 per volta per non occupare troppa RAM, mediante la funzione preparata "classifica" assegnata ai sottoprocessi
	while True:
		articoli = dbcursor.fetchmany(5000)
		#Interruzione del ciclo while quando la raccolta di nuove notizie da un insieme vuoto
		if len(articoli) == 0:
			break
		#Creazione ed assegnaemento del compito ai sottoprocessi
		pool = multiprocessing.Pool(initializer  = init, initargs = (vectorizer, clf, t0, progress, articlenum))
		pool.map(classifica, articoli)
		#Attesa dei sottoprocessi per procedere ad un nuovo insieme di articoli da classificare
		pool.close()
		pool.join()
	#Chiusura connessione principale
	dbcursor.close()
	dbconnection.close()
	
	#Fine script
	print("\n\n")
	print("\n---------- ESECUZIONE TERMINATA! ----------")

