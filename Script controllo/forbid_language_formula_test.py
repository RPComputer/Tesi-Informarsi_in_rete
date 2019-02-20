import joblib
import mysql.connector
from textblob import TextBlob
import nltk


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

print("---------- MODULO 3 - ESECUZIONE ----------\n")
print("----- Elaborazione frequenze parole -------\n")
'''
print("Connessione al database... ")
articleconnection = connect_to_db()
articlecursor = articleconnection.cursor();
print("completata\n")


print("Raccolta articoli...\n")
articlecursor.execute("SELECT * FROM articoli WHERE emptytext = 0 ORDER BY RAND()")
articoli = articlecursor.fetchmany(50)
joblib.dump(articoli, 'datasetProva50Articoli.pkl')
'''
articoli = joblib.load('datasetProva50Articoli.pkl')
wfrequency = joblib.load('dizionarioFrequenze.pkl')

error = 0
max = 100000
lentot = 0
lentotc = 0

for a in articoli:
	text = TextBlob(a[1])
	lunghezzadb = a[4]
	lunghezzatb = 0
	n = 0
	sf = 0
	for w in text.words:
		lunghezzatb += 1
		try:
			f = wfrequency[w]
		except:
			error += 1
			f = 0
		if f > 10 and f < max:
			n += 1
			sf += f
	mf = sf/n
	punteggio = 100 - mf*100/max
	lentot += lunghezzadb
	lentotc += lunghezzatb
	print("Punteggio: %0.2f", punteggio, " l db: ", lunghezzadb, " l tb: ", lunghezzatb)

print("Lunghezza totale db: ", lentot)
print("Lunghezza totale tb: ", lentotc)
print("Errori: ", error)
	
#Chiusura connessione principale
#articlecursor.close()
#articleconnection.close()




'''
massimo=0
wmassimo = ""
avg = 0
count = 0
n = 0

for key, value in wfrequency.items():
	if value > 10 and value < 1000000:
		count += value
		n += 1

avg = count/n
print("Massimo: ", wmassimo, " ", massimo)
print("Media: ", avg)

frequenze = list(wfrequency.values())
frequenze.sort()
print(len(frequenze))

for i in range(len(frequenze)):
	if frequenze[i] >= 1000000:
		print(i)
		print(frequenze[i])
		break
'''