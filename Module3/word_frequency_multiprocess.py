'''
Nome:
Calcolatore delle frequenze

Obiettivo:
Calcolare la frequenza di ogni parola negli articoli

Passaggi:
Collegarsi al database
Ottenere gli articoli
Effettuare l'analisi con TextBlob
Salvare i topic ottenuti ed il sentiment nel database
'''
import mysql.connector
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import nltk
import time
import multiprocessing
from multiprocessing import Manager
import joblib

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
def init(p, a, wd):
	#Ottine le variabili globali dal processo principale
	global progress
	global n_articoli
	global word_dict
	progress = p
	n_articoli = a
	word_dict = wd

#Funzione che si occupa, dato un insieme di topic e un articolo, di salvare opportunamente le informazioni nel database
def insert_frequencies(af, dizionario):
	#Per ogni parola inserisco la sua frequenza nel dizionario
	with dizionario.get_lock():
		for key, value in af.items():
			if key in dizionario.keys():
				dizionario[key] = dizionario[key] + value
			else:
				dizionario[key] = value
	


#Funzione che si occupa di effettuare l'analisi di un articolo e poi chiama l'inserimento delle informazioni
def article_handler(a):
	#Inizializzazione dell'oggetto blob, la sua creazione implica automaticamente l'analisi del testo
	text = TextBlob(a[1])
	#Acquisizione risultati dell'analisi dai campi dell'oggetto
	article_frequencies = text.word_counts
	
	#Inserimento frequenze nel dizionario globale
	insert_frequencies(article_frequencies, word_dict)
	
	#Output di aggiornamento
	with progress.get_lock():
		progress.value += 1
	percentage = (progress.value/n_articoli.value)*100
	print("Avanzamento: %0.3f" % percentage, "% \t", progress.value, "/", n_articoli.value, end='\r')
	
#Inizio script
#Gestione del processo principale
if __name__ == "__main__":
	print("---------- MODULO 3 - ESECUZIONE ----------\n")
	print("----- Elaborazione frequenze parole -------\n")
	print("Connessione al database... ")
	articleconnection = connect_to_db()
	articlecursor = articleconnection.cursor();
	print("completata\n")
	
	#Inizializzazione delle variabili
	n_articoli_tot = 386581
	n_articoli  = 380475
	n_articoli_empty = n_articoli_tot - n_articoli


	progress = multiprocessing.Value('i')
	with progress.get_lock():
		progress.value = 0

	print("Statistiche articoli:")
	print("Articoli: ", n_articoli_tot)
	print("Articoli analizzabili: ", n_articoli)
	print("Articoli non analizzabili: ", n_articoli_empty)

	#Dizionario frequenze delle parole
	manager = Manager()
	wfrequency = manager.dict()

	print("Raccolta articoli...\n")
	articlecursor.execute("SELECT * FROM articoli WHERE emptytext = 0")


	print("Articoli ottenuti\n")
	print("Analisi articoli - Calcolo frequenze parole in corso...\n")

	#Elaborazione degli articoli, 3000 per volta per non occupare troppa RAM, mediante la funzione preparata "article_handler" assegnata ai sottoprocessi
	while True:
		fetch_flag = False
		#Caricamento di 3000 articoli per volta al fine di non occupare troppa RAM, gestione degli errori per riconnessione
		while fetch_flag == False:
			try:
				articoli = articlecursor.fetchmany(3000)
				fetch_flag = True
			except:
				fetch_flag = False
				print("Persa connessione al database")
			'''
			if fetch_flag == False:
				articleconnection = connect_to_db()
				articlecursor = articleconnection.cursor();
				articlecursor.execute("SELECT * FROM articoli WHERE emptytext = 0 AND link NOT IN (SELECT DISTINCT articolo FROM articolitopic)")
			'''
		#Interruzione del ciclo while quando la raccolta di nuove notizie da un insieme vuoto
		if articoli == ():
			break
		#Creazione ed assegnaemento del compito ai sottoprocessi
		#pool.map_async(article_handler, articoli)
		pool = multiprocessing.Pool(initializer = init, initargs = (progress, n_articoli, wfrequency))
		pool.map(article_handler, articoli)
		#Attesa dei sottoprocessi per procedere ad un nuovo insieme di articoli da classificare
		pool.close()
		pool.join()
	
	joblib.dump(wfrequency, 'dizionarioFrequenze.pkl')
	
	#Chiusura connessione principale
	articlecursor.close()
	articleconnection.close()


	#Fine script

	print("\n---------- ESECUZIONE TERMINATA! ----------")