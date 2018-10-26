import mysql.connector
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
#from ... import ... importazione dell'algoritmo deciso

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
		
print("--------------------------- MODULO 2 - ESECUZIONE ---------------------\n")
print("------- Elaborazione categorie articoli - Train classificatore--------\n")

print("Connessione al database... ")
dbconnection = connect_to_db()
dbcursor = dbconnection.cursor();
print("completata\n")

print("Raccolta dataset...\n")
dbcursor.execute("SELECT testo, categoria FROM articoli WHERE empty_text = 0 AND categoria IS NOT NULL")
dataset_train = dbcursor.fetchall()

dbcursor.close()
dbconnection.close()
print("Preparazione al train")
testi_train, categorie_train = zip(*dataset_train)

vectorizer = TfidfVectorizer(decode_error='ignore', max_df=0.85)

x_train = vectorizer.fit_transform(testi_train)

#clf = sostituire con l'algoritmo definitivo

print("Avvio training...")
t0 = time()
clf.fit(x_train, categorie_train)
train_time = time() - t0
print("Train time: %0.3fs" % train_time)

print("Salvataggio modello..")
joblib.dump(clf, 'category_classification_model.pkl')

print("\n\n")
print("\n---------- ESECUZIONE TERMINATA! ----------")


'''

joblib.dump(clf, 'filename.pkl') 
clf_from_joblib = joblib.load('filename.pkl') 
clf_from_joblib.predict(X)

'''