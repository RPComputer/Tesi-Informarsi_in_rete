'''
Nome:
Calcolatore della qualità degli articoli

Obiettivo:
Calcolare la qualità del linguaggio utilizzato e del testo in generale

Passaggi:
Collegarsi al database
Ottenere gli articoli
Effettuare l'analisi con TextBlob
Calcolare la qualità
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
	global wfrequency
	progress = p
	n_articoli = na
	wfrequency = wd

#Funzione che si occupa, dato un insieme di topic e un articolo, di salvare opportunamente le informazioni nel database
def insert_data(article, ric, quality, cursor):
	data_query = ("UPDATE articoli SET pt_linguaggio = %s, pt_quality = %s WHERE link = %s")
	data = (ric, quality, article)
	try:
		cursor.execute(data_query, data)
	except mysql.connector.Error as e:
		print("\nErrore durante inserimento sentiment")
		print(e)

def coeff_entity(l, cursor):
	query = "SELECT COUNT(*) FROM articolitopic WHERE articolo = %s"
	cursor.execute(query, (l,))
	(n,) = cursor.fetchone()
	if n<10:
		return 0.40
	elif n<20:
		return 0.45
	elif n<25:
		return 0.50
	elif n<30:
		return 0.55
	elif n<35:
		return 0.60
	elif n<40:
		return 0.65
	elif n<45:
		return 0.70
	elif n<55:
		return 0.80
	elif n<75:
		return 0.85
	elif n<90:
		return 0.90
	elif n<150:
		return 0.95
	else:
		return 1
	
def coeff_lunghezza(n):
	if n<100:
		return 0.15
	elif n<150:
		return 0.20
	elif n<200:
		return 0.25
	elif n<250:
		return 0.30
	elif n<300:
		return 0.40
	elif n<350:
		return 0.55
	elif n<400:
		return 0.60
	elif n<450:
		return 0.70
	elif n<500:
		return 0.75
	elif n<550:
		return 0.80
	elif n<600:
		return 0.85
	elif n<650:
		return 0.90
	elif n<700:
		return 0.95
	else:
		return 1
	
def coeff_ricercatezza(t):
	global wfrequency
	text = TextBlob(t)
	n = 0
	sf = 0
	for w in text.words:
		try:
			f = wfrequency[w]
		except:
			f = 0
		if f > 10 and f < 100000:
			n += 1
			sf += f
	try:
		mf = sf/n
		punteggio = 1 - mf/100000
	except:
		punteggio = 0.3
	return punteggio

#Funzione che si occupa di effettuare l'analisi di un articolo e poi chiama l'inserimento delle informazioni
def article_handler(a):
	dbconnection = connect_to_db()
	dbcursor = dbconnection.cursor()
	cl = coeff_lunghezza(a[4])
	cr = coeff_ricercatezza(a[1])
	ce = coeff_entity(a[0], dbcursor)
	
	M = max(cl, ce)
	m = min(cl, ce)
	x = M/(M+m)
	y = 1-x
	
	punteggio = int(100*((2*cr+(x*M+y*m))/3))
	
	#Inserimento frequenze nel dizionario globale
	insert_data(a[0], cr, punteggio, dbcursor)
	dbconnection.commit()
	dbcursor.close()
	dbconnection.close()
	
	#Output di aggiornamento
	with progress.get_lock():
		progress.value += 1
	percentage = (progress.value/n_articoli)*100
	print("Avanzamento: %0.3f" % percentage, "% \t", progress.value, "/", n_articoli, end='\r')
	
	
#Inizio script
#Gestione del processo principale
if __name__ == "__main__":
	print("---------- MODULO 3 - ESECUZIONE ----------\n")
	print("----- Elaborazione qualità articoli -------\n")
	print("Connessione al database... ")
	articleconnection = connect_to_db()
	articlecursor = articleconnection.cursor();
	print("completata\n")
	
	#Inizializzazione delle variabili
	n_articoli_tot = 386581
	n_articoli  = 380475
	n_articoli_empty = n_articoli_tot - n_articoli
	
	wfrequency = joblib.load('dizionarioFrequenze.pkl')

	articlecursor.execute("SELECT COUNT(*) FROM articoli WHERE pt_linguaggio IS NOT NULL")
	(progressbase,) = articlecursor.fetchone()
	
	progress = multiprocessing.Value('i')
	with progress.get_lock():
		progress.value = progressbase

	print("Statistiche articoli:")
	print("Articoli: ", n_articoli_tot)
	print("Articoli analizzabili: ", n_articoli)
	print("Articoli non analizzabili: ", n_articoli_empty)

	print("Raccolta articoli...\n")
	articlecursor.execute("SELECT * FROM articoli WHERE emptytext = 0 AND pt_linguaggio IS NULL")


	print("Articoli ottenuti\n")
	print("Analisi articoli - Calcolo qualità in corso...\n")

	#Elaborazione degli articoli, 3000 per volta per non occupare troppa RAM, mediante la funzione preparata "article_handler" assegnata ai sottoprocessi
	while True:
		fetch_flag = False
		#Caricamento di 3000 articoli per volta al fine di non occupare troppa RAM, gestione degli errori per riconnessione
		while fetch_flag == False:
			print("\n2 secondi per chiudere...\n")
			time.sleep(2)
			try:
				articoli = articlecursor.fetchmany(3000)
				fetch_flag = True
			except:
				fetch_flag = False
				print("Persa connessione al database")
			if fetch_flag == False:
				articleconnection = connect_to_db()
				articlecursor = articleconnection.cursor();
				articlecursor.execute("SELECT * FROM articoli WHERE emptytext = 0 AND pt_linguaggio IS NULL")

		#Interruzione del ciclo while quando la raccolta di nuove notizie da un insieme vuoto
		if len(articoli) == 0:
			break
		#Creazione ed assegnaemento del compito ai sottoprocessi
		#pool.map_async(article_handler, articoli)
		pool = multiprocessing.Pool(initializer = init, initargs = (progress, n_articoli, wfrequency))
		pool.map(article_handler, articoli)
		#Attesa dei sottoprocessi per procedere ad un nuovo insieme di articoli da classificare
		pool.close()
		pool.join()
	
	#Chiusura connessione principale
	articlecursor.close()
	articleconnection.close()


	#Fine script

	print("\n---------- ESECUZIONE TERMINATA! ----------")