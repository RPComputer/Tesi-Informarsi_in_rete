import joblib
import mysql.connector


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
print("----- Raccolta dataset 1 quesito -------\n")

print("Connessione al database... ")
articleconnection = connect_to_db()
articlecursor = articleconnection.cursor();
print("completata\n")


print("Raccolta articoli...\n")
articlecursor.execute("SELECT topic, COUNT(*) AS conteggio FROM articolitopic GROUP BY topic ORDER BY conteggio DESC")
topic = articlecursor.fetchall()
joblib.dump(topic, 'dataset3Argomenti.pkl')

#Chiusura connessione principale
articlecursor.close()
articleconnection.close()

for t in topic:
	print(t)
