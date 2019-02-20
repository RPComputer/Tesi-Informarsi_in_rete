import mysql.connector
import joblib
#Funzione di connessione al database
def connect_to_db():
	try:
		res = mysql.connector.connect(user='module1', password='insertnews', host='localhost', database='tesi', charset="utf8", use_unicode=True)
		return res
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("\nPassword e/o username errati")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("\nDatabase does not exist")
		else:
			print("\nErrore: " + err)
		return None

#Inizio script
print("---------- MODULO 3 - ESECUZIONE ----------\n")
print("-------- Calcolo valori topic -------------\n")
print("Connessione al database... ")
newsconnection = connect_to_db()
newscursor = newsconnection.cursor();
print("completata\n")

newscursor.execute("SELECT COUNT(*) FROM articolitopic GROUP BY articolo")
entity = newscursor.fetchall()
joblib.dump(entity, 'entityNumber.pkl')
newscursor.close()
newsconnection.close()

entitypure = [x[0] for x in entity]

media = sum(entitypure)/len(entitypure)
massimo = max(entitypure)
minimo = min(entitypure)

print("Media: ", media)
print("Massimo: ", massimo)
print("Minimo: ", minimo)