import mysql.connector
import joblib
from operator import itemgetter

'''
sb.set(style="darkgrid")
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
dbcursor.execute("SELECT MIN(a.pt_quality), MAX(a.pt_quality), AVG(a.pt_quality), n.sitoweb FROM articoli AS a JOIN notizie AS n ON a.link = n.dlink WHERE a.pt_quality IS NOT NULL GROUP BY n.sitoweb")
qs = dbcursor.fetchall()
'''
#joblib.dump(qs, 'qualitaSito.pkl')
qs = joblib.load('qualitaSito.pkl')

#print(qs)

qs = sorted(qs,key=itemgetter(2), reverse=True)
joblib.dump(qs, 'qualitaSitoOrd.pkl')
'''
for x in qs:
	print(x)
'''
'''
#Chiusura connessione
dbcursor.close()
dbconnection.close()
'''

#Fine script

print("\n---------- ESECUZIONE TERMINATA! ----------")