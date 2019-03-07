import joblib
import mysql.connector

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
print("----- Verifica classificazione di salute e benessere -------\n")
'''
print("Connessione al database... ")
articleconnection = connect_to_db()
articlecursor = articleconnection.cursor();
print("completata\n")


print("Raccolta articoli...\n")
articlecursor.execute("SELECT n.sitoweb, a.link FROM articoli AS a JOIN notizie AS n ON a.link = n.dlink WHERE ce_flag = 1 AND categoria = 'salute e benessere'")
notizie = articlecursor.fetchall()
joblib.dump(notizie, 'verificaSaluteBen.pkl')
'''
notizie = joblib.load('verificaSaluteBen.pkl')
#file = open("responso.txt", 'w')
res = open("giornaliProb.txt", 'w')
d = dict()
'''
articoli = joblib.load('datasetProva50Articoli.pkl')
wfrequency = joblib.load('dizionarioFrequenze.pkl')
'''
for n in notizie:
	if n[0] in d.keys():
		d[n[0]]+=1
	else:
		d[n[0]]=1
		
res.write(str(d))
	
res.close()
#Chiusura connessione principale
#articlecursor.close()
#articleconnection.close()
