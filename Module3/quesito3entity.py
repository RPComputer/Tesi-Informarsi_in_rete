import mysql.connector
import joblib
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sb
from operator import itemgetter

sb.set(style="darkgrid")

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
print("------ Elaborazione query qualità notizieper sito -----\n")
'''
print("Connessione al database... ")
dbconnection = connect_to_db()
dbcursor = dbconnection.cursor();
print("completata\n")

entity = joblib.load('dictEntityFreq.pkl')

entitySorted = sorted(entity.items(), reverse = True, key=lambda kv: kv[1])


for i in range(100):
	print(entitySorted[i])

query_trump = "SELECT s.paese, a.pol_sentiment FROM articolitopic AS atp JOIN articoli AS a ON atp.articolo = a.link JOIN notizie AS n ON a.link = n.dlink JOIN sitiweb AS s ON n.sitoweb = s.nome WHERE atp.topic = 'donald trump' OR atp.topic = 'trump'"
query_europe = "SELECT s.paese, a.pol_sentiment FROM articolitopic AS atp JOIN articoli AS a ON atp.articolo = a.link JOIN notizie AS n ON a.link = n.dlink JOIN sitiweb AS s ON n.sitoweb = s.nome WHERE atp.topic = 'europe' OR atp.topic = 'europa'"
query_italy = "SELECT s.paese, a.pol_sentiment FROM articolitopic AS atp JOIN articoli AS a ON atp.articolo = a.link JOIN notizie AS n ON a.link = n.dlink JOIN sitiweb AS s ON n.sitoweb = s.nome WHERE atp.topic = 'italy' OR atp.topic = 'italia'"

print("Raccolta dati entità trump...")
dbcursor.execute(query_trump)
result_t = dbcursor.fetchall()
print("Raccolta dati entità europa...")
dbcursor.execute(query_europe)
result_e = dbcursor.fetchall()
print("Raccolta dati entità italia...")
dbcursor.execute(query_italy)
result_i = dbcursor.fetchall()


print("Dumping...")
joblib.dump(result_t, 'datasetTrump.pkl')
joblib.dump(result_e, 'datasetEuropa.pkl')
joblib.dump(result_i, 'datasetItalia.pkl')

#Chiusura connessione
dbcursor.close()
dbconnection.close()
'''
#------------------------------------------------------------------------------------
print("Raccolta dati...")
result_t = joblib.load('datasetTrump.pkl')
result_e = joblib.load('datasetEuropa.pkl')
result_i = joblib.load('datasetItalia.pkl')

print("Preparazione dati...")
dataset_t = pd.DataFrame(result_t, columns=["Paese","Sentiment"])
dataset_e = pd.DataFrame(result_e, columns=["Paese","Sentiment"])
dataset_i = pd.DataFrame(result_i, columns=["Paese","Sentiment"])

dataset_t['Entity'] = 'Donald Trump'
dataset_e['Entity'] = 'Europe'
dataset_i['Entity'] = 'Italy'


'''
concatenated = pd.concat([dataset_t,dataset_e,dataset_i])
grafico = sb.boxplot(x="Sentiment", y="Entity", data=concatenated)
plt.show()
'''
grafico1 = sb.boxplot(x="Sentiment", y="Paese", data=dataset_t)
plt.show()
grafico2 = sb.boxplot(x="Sentiment", y="Paese", data=dataset_e)
plt.show()
grafico3 = sb.boxplot(x="Sentiment", y="Paese", data=dataset_i)
plt.show()

#Fine script

print("\n---------- ESECUZIONE TERMINATA! ----------")