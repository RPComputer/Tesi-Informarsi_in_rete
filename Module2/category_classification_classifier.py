import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
from time import time

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
print("---------- Elaborazione categorie articoli - Classificazione-----------\n")

print("Connessione al database... ")
dbconnection = connect_to_db()
dbcursor = dbconnection.cursor();
print("completata\n")

print("Raccolta articoli da classificare...\n")
dbcursor.execute("SELECT link, testo FROM articoli WHERE empty_text = 0 AND categoria IS NULL")
articoli = dbcursor.fetchall()

print("Caricamento classificatore")
clf = joblib.load('category_classification_model.pkl')

progress = 0
articlenum = len(articoli)


vectorizer = TfidfVectorizer(decode_error='ignore', max_df=0.85)

print("Avvio classificazione...")
t0 = time()

for a in articoli:
  testo = vectorizer.transform(a[1])
  categoria = clf.predict(testo)
  
  cat_query = ("UPDATE articoli SET categoria WHERE link VALUES (%s, %s)")
  cat_data = (categoria, a[0])
  dbcursor.execute(cat_query, cat_data)
  
  t = time() - t0
  progress = progress + 1
	percentage = progress/articlenum*100
  print("Avanzamento: ", percentage, "%   ", progress, "/", articlenum, "   -   Tempo trascorso: %0.3fs" % t, end='\r')
  

dbcursor.close()
dbconnection.close()

print("\n\n")
print("\n---------- ESECUZIONE TERMINATA! ----------")


'''

joblib.dump(clf, 'filename.pkl') 
clf_from_joblib = joblib.load('filename.pkl') 
clf_from_joblib.predict(X)

'''