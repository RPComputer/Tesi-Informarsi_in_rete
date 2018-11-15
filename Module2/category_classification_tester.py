import mysql.connector
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from sklearn import linear_model
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import ComplementNB
from sklearn.linear_model import PassiveAggressiveClassifier


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
print("------- Elaborazione categorie articoli - Tester calssificatori--------\n")

print("Connessione al database... ")
dbconnection = connect_to_db()
dbcursor = dbconnection.cursor(buffered=True);
print("completata\n")

print("Raccolta dataset...\n")
dbcursor.execute("SELECT testo, categoria FROM articoli WHERE emptytext = 0 AND categoria IS NOT NULL")
dataset_train = dbcursor.fetchmany(2000)
dataset_test = dbcursor.fetchmany(1000)

dbcursor.close()
dbconnection.close()

testi_train, categorie_train = zip(*dataset_train)
testi_test, categorie_test = zip(*dataset_test)

vectorizer = TfidfVectorizer(decode_error='ignore', max_df=0.85)

x_train = vectorizer.fit_transform(testi_train).todense()
x_test = vectorizer.fit_transform(testi_test).todense()

def benchmark(clf):
	t0 = time()
	clf.fit(x_train, categorie_train)
	train_time = time() - t0
	print("Train time: %0.3fs" % train_time)
	t0 = time()
	pred = clf.predict(x_test)
	test_time = time() - t0
	print("Test time: %0.3fs" % test_time)
	score = metrics.accuracy_score(categorie_test, pred)
	print("Accuratezza: %0.3f" % score)
	

#SGDClassifier
print("SGDClassifier test")
SDGC = SGDClassifier(penalty='l2', n_jobs=-1)
benchmark(SDGC)
print("\n\n")
#ComplementNB
print("ComplementNB test")
CNB = ComplementNB()
benchmark(CNB)
print("\n\n")
#PassiveAggressiveClassifier
print("PassiveAggressiveClassifier test")
PAC = PassiveAggressiveClassifier(max_iter=50, n_jobs=-1)
benchmark(PAC)
print("\n\n")
print("\n---------- ESECUZIONE TERMINATA! ----------")