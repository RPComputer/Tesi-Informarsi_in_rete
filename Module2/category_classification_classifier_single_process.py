'''
Nome:
Classificatore degli articoli

Obiettivo:
Classificare tutti gli articoli nelle categorie prescelte mediante il modello precedentemente preparato

Passaggi:
Collegarsi al database
Ottenere gli articoli
Effettuare la classificazione dell'insieme di articoli ottenuto, uno per volta
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

#Funzione che si occupa di classificare un articolo e salvarne la categoria nel database
def classifica(a):
	#Acuisizione delle variabili globali
	global progress
	global t0
	global clf
	global vectorizer
	global articlenum
	#Preparazione dei dati: trasformazione del testo in matrice numeriche per migliorare l'efficenza del codice mediante sempre il medesimo trasformatore
	testo = vectorizer.transform([a[1]])
	#Classificazione del testo
	categoria = clf.predict(testo)
	#Salvataggio nel database della categoria
	insertconnection = connect_to_db()
	insertcursor = insertconnection.cursor()
	cat_query = ("UPDATE articoli SET categoria = %s, ce_flag = %s WHERE link = %s")
	cat_data = (str(categoria[0]), 1, str(a[0]))
	insertcursor.execute(cat_query, cat_data)
	#Chiusura connessione
	insertconnection.commit()
	insertcursor.close()
	insertconnection.close()
	#Output di aggiornamento
	t = time() - t0
	progress += 1
	percentage = progress/articlenum*100
	print("Avanzamento: ", percentage, "%   ", progress, "/", articlenum, "   -   Tempo trascorso: %0.3fs" % t, end='\r')

#Inizio script
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

progress = 0
articlenum = 163008

print("Avvio classificazione...")
t0 = time()

#Classificazione degli articoli, 5000 per volta per non occupare troppa RAM, mediante la funzione preparata "classifica"
while True:
	articoli = dbcursor.fetchmany(5000)
	#Interruzione del ciclo while quando la raccolta di nuovi articoli da un insieme vuoto
	if len(articoli) == 0:
		break
	for a in articoli:
		classifica(a)

#Chiusura connessione principale
dbcursor.close()
dbconnection.close()

#Fine script
print("\n---------- ESECUZIONE TERMINATA! ----------")
