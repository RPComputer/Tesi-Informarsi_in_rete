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

def classifica(a):
	global progress
	global t0
	global clf
	global vectorizer
	global articlenum
	testo = vectorizer.transform([a[1]])
	categoria = clf.predict(testo)
	
	insertconnection = connect_to_db()
	insertcursor = insertconnection.cursor()
	cat_query = ("UPDATE articoli SET categoria = %s, ce_flag = %s WHERE link = %s")
	cat_data = (str(categoria[0]), 1, str(a[0]))
	insertcursor.execute(cat_query, cat_data)
	
	insertconnection.commit()
	insertcursor.close()
	insertconnection.close()

	t = time() - t0
	progress += 1
	percentage = progress/articlenum*100
	print("Avanzamento: ", percentage, "%   ", progress, "/", articlenum, "   -   Tempo trascorso: %0.3fs" % t, end='\r')

print("--------------------------- MODULO 2 - ESECUZIONE ---------------------\n")
print("---------- Elaborazione categorie articoli - Classificazione-----------\n")

print("Connessione al database... ")
dbconnection = connect_to_db()
dbcursor = dbconnection.cursor();
print("completata\n")

print("Raccolta articoli da classificare...\n")
dbcursor.execute("SELECT link, testo FROM articoli WHERE emptytext = 0 AND categoria IS NULL")


print("Caricamento classificatore")
clf = joblib.load('category_classification_model.pkl')

vectorizer = joblib.load('category_classification_vectorizer.pkl')

progress = 0
articlenum = 163008

print("Avvio classificazione...")
t0 = time()

while True:
	articoli = dbcursor.fetchmany(5000)
	if len(articoli) == 0:
		break
	for a in articoli:
		classifica(a)

dbcursor.close()
dbconnection.close()

print("\n---------- ESECUZIONE TERMINATA! ----------")


'''

joblib.dump(clf, 'filename.pkl') 
clf_from_joblib = joblib.load('filename.pkl') 
clf_from_joblib.predict(X)

'''