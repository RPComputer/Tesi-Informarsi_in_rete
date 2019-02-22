import mysql.connector
import joblib
from operator import itemgetter
'''
#Funzione di connessione al database
def connect_to_db():
	try:
		res = mysql.connector.connect(user='module1', password='insertnews', host='2.224.109.7', database='tesi')
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
print("------ Elaborazione query qualità notizieper sito -----\n")

print("Connessione al database... ")
dbconnection = connect_to_db()
dbcursor = dbconnection.cursor();
print("completata\n")

print("Raccolta del dataset...")
dbcursor.execute("SELECT MIN(a.pt_linguaggio), MAX(a.pt_linguaggio), AVG(a.pt_linguaggio), n.sitoweb FROM articoli AS a JOIN notizie AS n ON a.link = n.dlink WHERE a.pt_linguaggio IS NOT NULL GROUP BY n.sitoweb")
qs = dbcursor.fetchall()

#

#print(qs)

qs = sorted(qs,key=itemgetter(2), reverse=True)
joblib.dump(qs, 'ricercatezzaLinguaggioSito.pkl')
'''
qs = joblib.load('ricercatezzaLinguaggioSito.pkl')

i=1
for x in qs:
	print(x, i)
	i+=1
'''
#Chiusura connessione
dbcursor.close()
dbconnection.close()
'''

#Fine script

print("\n---------- ESECUZIONE TERMINATA! ----------")