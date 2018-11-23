import mysql.connector
import time
from sklearn.externals import joblib
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier

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

print("\n\n--------------------------- MODULO 2 - ESECUZIONE ---------------------\n")
print("------- Elaborazione categorie articoli - Tester calssificatori--------\n")

print(" Connessione al database... ")
dbconnection = connect_to_db()
dbcursor = dbconnection.cursor(buffered=True);
print(" completata\n")

print(" Avvio training...\n")
dbcursor.execute("SELECT testo, categoria FROM articoli WHERE emptytext = 0 AND categoria IS NOT NULL")
start_time = time.time()
vectorizer = HashingVectorizer(decode_error='ignore', n_features=2 ** 18, alternate_sign=False)
classi = ["esteri","politica","economia","cronaca","scienza e tecnologia","sport","cultura e intrattenimento","salute e benessere","altro"]

total_time = 0

cls = SGDClassifier(penalty='l2', n_jobs=-1)
	
while True:
	dataset_train = dbcursor.fetchmany(2500)
	if len(dataset_train) == 0:
		break
	t0 = time.time()
	testi_train, categorie_train = zip(*dataset_train)
	X_train = vectorizer.transform(testi_train)
	
	cls.partial_fit(X_train, categorie_train, classi)
	total_time += time.time() - t0
	passed_time = time.time()-start_time
	print("Training in corso - Tempo trascorso %0.3fs" % passed_time, "Tempo training: %0.3fs" % total_time)


print("Salvataggio modello..")
joblib.dump(cls, 'category_classification_model.pkl')
joblib.dump(vectorizer, 'category_classification_vectorizer.pkl')

print("\n\n")
print("\n---------- ESECUZIONE TERMINATA! ----------")


'''

joblib.dump(clf, 'filename.pkl') 
clf_from_joblib = joblib.load('filename.pkl') 
clf_from_joblib.predict(X)

'''