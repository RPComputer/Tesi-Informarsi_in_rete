'''
Nome:
Calcolatore delle frequenze

Obiettivo:
Calcolare la frequenza di ogni entity negli articoli per ottenere il dataset per il I quesito

'''
import mysql.connector
import joblib

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

entityDic = dict()
progress = 0

print("---------- MODULO 3 - ESECUZIONE ----------\n")
print("----- Raccolta dataset 1 quesito -------\n")

print("Connessione al database... ")
articleconnection = connect_to_db()
articlecursor = articleconnection.cursor();
print("completata\n")

print("Raccolta articoli...\n")
articlecursor.execute("SELECT topic FROM articolitopic")

while True:
	entity = articlecursor.fetchmany(5000)
	print("fetching 5000...")
	for e in entity:
		if e[0] in entityDic.keys():
			entityDic[e[0]] = entityDic[e[0]]+1
		else:
			entityDic[e[0]] = 1
		progress += 1
		print("Avanzamento: ", progress, end='\r')
	if len(entity) == 0:
		break

joblib.dump(entityDic, 'dictEntityFreq.pkl')

#Chiusura connessione principale
articlecursor.close()
articleconnection.close()

#Fine script

print("\n---------- ESECUZIONE TERMINATA! ----------")