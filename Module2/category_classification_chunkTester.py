import mysql.connector
import time
from sklearn import metrics
from sklearn import linear_model
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

total_articles = 0
total_time = 0

def benchmark(clf):
	t0 = time.time()
	pred = clf.predict(x_test)
	test_time = time.time() - t0
	print("  Test time: %0.3fs" % test_time)
	score = metrics.accuracy_score(categorie_test, pred)
	print("  Accuratezza: %0.3f" % score)

cls = SGDClassifier(penalty='l2', n_jobs=-1)
	
while total_articles < 200000:
	dataset_train = dbcursor.fetchmany(2500)
	total_articles += 2500
	t0 = time.time()
	testi_train, categorie_train = zip(*dataset_train)
	X_train = vectorizer.transform(testi_train)
	
	cls.partial_fit(X_train, categorie_train, classi)
	total_time += time.time() - t0
	passed_time = time.time()-start_time
	print("Training in corso - Tempo trascorso %0.3fs" % passed_time, "Tempo training: %0.3fs" % total_time)

dataset_test = dbcursor.fetchmany(1000)
dbcursor.close()
dbconnection.close()
testi_test, categorie_test = zip(*dataset_test)
x_test = vectorizer.transform(testi_test)
benchmark(cls)


print("\n")
print("\n---------- ESECUZIONE TERMINATA! ----------\n\n")
