'''
Nome:
Trainer del classificatore SGDC scelto

Obiettivo:
Effettuare il training del classificare SGDC sull'intero dataset di articoli e salvare il modello ottenuto

Passaggi:
Collegarsi al database
Ottenere gli articoli
Effettuare il training con l'insieme di articoli ottenuto
Salvare il modello ottenuto al fine di utilizzarlo per l'algoritmo di classificazione
'''
import mysql.connector
import time
from sklearn.externals import joblib
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier


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
print(" Avvio training...\n")
dbcursor.execute("SELECT testo, categoria FROM articoli WHERE emptytext = 0 AND categoria IS NOT NULL")
start_time = time.time()
vectorizer = HashingVectorizer(decode_error='ignore', n_features=2 ** 18, alternate_sign=False)
#Dichiarazione del vettore contenente le possibili classificazioni degli articoli, necessario per il modello di tranining
classi = ["esteri","politica","economia","cronaca","scienza e tecnologia","sport","cultura e intrattenimento","salute e benessere","altro"]

total_time = 0
#Inizializzazione del classificatore
cls = SGDClassifier(penalty='l2', n_jobs=-1)

#Training del classificatore con il dataset completo, per la gestione della RAM si effettua il training con 2500 articoli alla volta
while True:
	dataset_train = dbcursor.fetchmany(2500)
	#Interruzione del ciclo while quando la raccolta di nuove notizie da un insieme vuoto
	if len(dataset_train) == 0:
		break
	#Preparazione dei dati: spacchettamnto info raccolte e trasformazione dei testi in matrici numeriche per migliorare l'efficenza del codice
	t0 = time.time()
	testi_train, categorie_train = zip(*dataset_train)
	X_train = vectorizer.transform(testi_train)
	#Training parziale
	cls.partial_fit(X_train, categorie_train, classi)
	#Output di aggiornamento
	total_time += time.time() - t0
	passed_time = time.time()-start_time
	print("Training in corso - Tempo trascorso %0.3fs" % passed_time, "Tempo training: %0.3fs" % total_time)

#Salvataggio del modello di classificatore e trasformatore
print("Salvataggio modello..")
joblib.dump(cls, 'category_classification_model.pkl')
joblib.dump(vectorizer, 'category_classification_vectorizer.pkl')

#Fine script
print("\n\n")
print("\n---------- ESECUZIONE TERMINATA! ----------")

