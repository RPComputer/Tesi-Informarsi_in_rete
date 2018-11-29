'''
Nome:
Tester dei classificatori prescelti

Obiettivo:
Testare la validità dei 3 classificatori prescelti per selezionare il migliore da applicare

Passaggi:
Collegarsi al database
Ottenere gli articoli
Effettuare il training con l'insieme di articoli ottenuto, un classificare per volta
Testare l'abilità del classificatore di classificare un insieme di notizie di cui si conoscono già le categorie, uno per volta
'''
import mysql.connector
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from sklearn import linear_model
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import ComplementNB
from sklearn.linear_model import PassiveAggressiveClassifier

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

#Inizio script
print("\n\n--------------------------- MODULO 2 - ESECUZIONE ---------------------\n")
print("------- Elaborazione categorie articoli - Tester calssificatori--------\n")

print(" Connessione al database... ")
dbconnection = connect_to_db()
dbcursor = dbconnection.cursor(buffered=True);
print(" completata\n")

#Caricamento dataset ed inizializzazione delle variabili globali
print(" Raccolta dataset...\n")
dbcursor.execute("SELECT testo, categoria FROM articoli WHERE emptytext = 0 AND categoria IS NOT NULL")
dataset_train = dbcursor.fetchmany(2000)
dataset_test = dbcursor.fetchmany(1000)

print(" Raccolta completata\n\n\n")
#Chiusura connessione principale
dbcursor.close()
dbconnection.close()

#Preparazione dei dati: spacchettamnto info raccolte e trasformazione dei testi in matrici numeriche per migliorare l'efficenza del codice
testi_train, categorie_train = zip(*dataset_train)
testi_test, categorie_test = zip(*dataset_test)

vectorizer = TfidfVectorizer(decode_error='ignore', min_df=0.01, max_df=0.60)

x_train = vectorizer.fit_transform(testi_train).todense()
x_test = vectorizer.transform(testi_test).todense()

#Funzione per il test del modello dopo il training, calcolo tempi di test ed accuratezza delle classificazioni
def benchmark(clf):
	t0 = time()
	clf.fit(x_train, categorie_train)
	train_time = time() - t0
	print("  Train time: %0.3fs" % train_time)
	t0 = time()
	pred = clf.predict(x_test)
	test_time = time() - t0
	print("  Test time: %0.3fs" % test_time)
	score = metrics.accuracy_score(categorie_test, pred)
	print("  Accuratezza: %0.3f" % score)
	

#SGDClassifier
print(" SGDClassifier test:\n")
SDGC = SGDClassifier(penalty='l2', n_jobs=-1)
benchmark(SDGC)
print("\n\n")
#ComplementNB
print(" ComplementNB test:\n")
CNB = ComplementNB()
benchmark(CNB)
print("\n\n")
#PassiveAggressiveClassifier
print(" PassiveAggressiveClassifier test:\n")
PAC = PassiveAggressiveClassifier(max_iter=50, n_jobs=-1)
benchmark(PAC)

#Fine script
print("\n")
print("\n---------- ESECUZIONE TERMINATA! ----------\n\n")