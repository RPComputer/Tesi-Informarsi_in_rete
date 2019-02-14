'''
Nome:
Calcolatore delle frequenze

Obiettivo:
Calcolare la frequenza di ogni parola negli articoli e aggiiornare il sentiment

Passaggi:
Collegarsi al database
Ottenere gli articoli
Effettuare l'analisi con TextBlob
Salvare le frequenze nel dizionario e il sentiment sul database
'''
import mysql.connector
from textblob import TextBlob
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
def init(p, na, wd):
	#Ottine le variabili globali dal processo principale
	global progress
	global n_articoli
	global word_dict
	progress = p
	n_articoli = na
	word_dict = wd

#Funzione che si occupa, dato un insieme di topic e un articolo, di salvare opportunamente le informazioni nel database
def insert_data(article, af, dizionario, gs, sent):
	#Nuova connessione per getire il salvataggio dei dati sul database
	insertconnection = connect_to_db()
	insertcursor = insertconnection.cursor()
	
	sentiment_query = ("UPDATE articoli SET sentiment = %s, pol_sentiment = %s WHERE link = %s")
	sentiment_data = (gs, sent, article[0])
	try:
		insertcursor.execute(sentiment_query, sentiment_data)
	except mysql.connector.Error as e:
		print("\nErrore durante inserimento sentiment")
		print(e)
	
	#Chiusura connessione deicata
	insertconnection.commit()
	insertcursor.close()
	insertconnection.close()
	#Per ogni parola inserisco la sua frequenza nel dizionario
	#with dizionario.get_lock():
	for key, value in af.items():
		if key in dizionario.keys():
			dizionario[key] = dizionario[key] + value
		else:
			dizionario[key] = value
	#joblib.dump(dizionario.copy(), 'dizionarioFrequenze.pkl')
	


#Funzione che si occupa di effettuare l'analisi di un articolo e poi chiama l'inserimento delle informazioni
def article_handler(a):
	#Inizializzazione dell'oggetto blob, la sua creazione implica automaticamente l'analisi del testo
	text = TextBlob(a[1])
	#Acquisizione risultati dell'analisi dai campi dell'oggetto
	article_frequencies = text.word_counts
	global_sentimet = text.sentiment[0]
	neg = 0
	pos = 0
	for f in text.sentences:
		if f.sentiment[0] < 0.0:
			neg += 1
		elif f.sentiment[0] > 0.0:
			pos += 1

	if pos+neg != 0:
		sentiment_calcolato = (pos-neg)/(pos+neg)
	else:
		sentiment_calcolato = 0
	
	#Inserimento frequenze nel dizionario globale
	insert_data(a, article_frequencies, word_dict, global_sentimet, sentiment_calcolato)
	
	#Output di aggiornamento
	with progress.get_lock():
		progress.value += 1
	percentage = (progress.value/n_articoli)*100
	print("Avanzamento: %0.3f" % percentage, "% \t", progress.value, "/", n_articoli, end='\r')
	
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

	articlecursor.execute("SELECT COUNT(*) FROM articoli WHERE sentiment IS NOT NULL")
	(progressbase,) = articlecursor.fetchone()
	
	progress = multiprocessing.Value('i')
	with progress.get_lock():
		progress.value = progressbase

	print("Statistiche articoli:")
	print("Articoli: ", n_articoli_tot)
	print("Articoli analizzabili: ", n_articoli)
	print("Articoli non analizzabili: ", n_articoli_empty)

	#Dizionario frequenze delle parole
	manager = Manager()
	wfrequency = manager.dict()
	
	try:
		saved_dict = joblib.load('dizionarioFrequenze.pkl')
		wfrequency.update(saved_dict)
	except:
		pass

	print("Raccolta articoli...\n")
	articlecursor.execute("SELECT * FROM articoli WHERE emptytext = 0 AND sentiment IS NULL")


	print("Articoli ottenuti\n")
	print("Analisi articoli - Calcolo frequenze parole in corso...\n")

	#Elaborazione degli articoli, 3000 per volta per non occupare troppa RAM, mediante la funzione preparata "article_handler" assegnata ai sottoprocessi
	while True:
		fetch_flag = False
		#Caricamento di 3000 articoli per volta al fine di non occupare troppa RAM, gestione degli errori per riconnessione
		while fetch_flag == False:
			joblib.dump(wfrequency.copy(), 'dizionarioFrequenze.pkl')
			print("\n3 secondi per chiudere...\n")
			time.sleep(3)
			try:
				articoli = articlecursor.fetchmany(3000)
				fetch_flag = True
			except:
				fetch_flag = False
				print("Persa connessione al database")
			if fetch_flag == False:
				articleconnection = connect_to_db()
				articlecursor = articleconnection.cursor();
				articlecursor.execute("SELECT * FROM articoli WHERE emptytext = 0 AND sentiment IS NULL")

		#Interruzione del ciclo while quando la raccolta di nuove notizie da un insieme vuoto
		if len(articoli) == 0:
			break
		#Creazione ed assegnaemento del compito ai sottoprocessi
		#pool.map_async(article_handler, articoli)
		pool = multiprocessing.Pool(processes=4, initializer = init, initargs = (progress, n_articoli, wfrequency))
		pool.map(article_handler, articoli)
		#Attesa dei sottoprocessi per procedere ad un nuovo insieme di articoli da classificare
		pool.close()
		pool.join()
	
	joblib.dump(wfrequency.copy(), 'dizionarioFrequenze.pkl')
	
	#Chiusura connessione principale
	articlecursor.close()
	articleconnection.close()


	#Fine script

	print("\n---------- ESECUZIONE TERMINATA! ----------")