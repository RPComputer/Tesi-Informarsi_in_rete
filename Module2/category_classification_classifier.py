import mysql.connector
from sklearn.externals import joblib
from time import time
import multiprocessing

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

def init(v, c, t, p, a):
	global vectorizer
	global clf
	global t0
	global progress
	global articlenum
	vectorizer = v
	clf = c
	t0 = t
	progress = p
	articlenum = a

def classifica(a):
	testo = vectorizer.transform(a[1])
	categoria = clf.predict(testo)
	
	insertconnection = connect_to_db()
	insertcursor = insertconnection.cursor()
	
	cat_query = ("UPDATE articoli SET categoria, ce_flag WHERE link VALUES (%s, %s, %s)")
	cat_data = (categoria, 1, a[0])
	insertcursor.execute(cat_query, cat_data)
	
	insertconnection.commit()
	insertcursor.close()
	insertconnection.close()

	t = time() - t0.value
	with progress.get_lock():
		progress.value += 1
	percentage = progress.value/articlenum.value*100
	print("Avanzamento: ", percentage, "%   ", progress.value, "/", articlenum.value, "   -   Tempo trascorso: %0.3fs" % t, end='\r')

print("--------------------------- MODULO 2 - ESECUZIONE ---------------------\n")
print("---------- Elaborazione categorie articoli - Classificazione-----------\n")

print("Connessione al database... ")
dbconnection = connect_to_db()
dbcursor = dbconnection.cursor();
print("completata\n")

print("Raccolta articoli da classificare...\n")
dbcursor.execute("SELECT link, testo FROM articoli WHERE empty_text = 0 AND categoria IS NULL")


print("Caricamento classificatore")
clf = joblib.load('category_classification_model.pkl')

vectorizer = joblib.load('category_classification_vectorizer.pkl')

progress = multiprocessing.Value('i')
with progress.get_lock():
	progress.value = 0
articlenum = multiprocessing.Value('i')
with articlenum.get_lock():
	articlenum.value = 163008



print("Avvio classificazione...")
t0 = multiprocessing.Value('f')
with t0.get_lock():
	t0.value = time()

while True:
	articoli = dbcursor.fetchmany(2500)
	if len(articoli) == 0:
		break
	pool = multiprocessing.Pool(initializer  = init, initargs = (vectorizer, clf, t0, progress, articlenum))
	pool.map(classifica, articoli)
	pool.close()
	pool.join()

dbcursor.close()
dbconnection.close()

print("\n\n")
print("\n---------- ESECUZIONE TERMINATA! ----------")


'''

joblib.dump(clf, 'filename.pkl') 
clf_from_joblib = joblib.load('filename.pkl') 
clf_from_joblib.predict(X)

'''