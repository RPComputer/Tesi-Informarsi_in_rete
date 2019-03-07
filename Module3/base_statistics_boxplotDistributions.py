import mysql.connector
import joblib
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sb

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
print("------ Statistiche di base, distribuzione con boxplot -----\n")

print("Connessione al database... ")
dbconnection = connect_to_db()
dbcursor = dbconnection.cursor();
print("completata\n")

query_quality = "SELECT pt_quality FROM articoli WHERE emptytext = 0"
query_sentiment = "SELECT sentiment FROM articoli WHERE emptytext = 0"
query_sentiment_perpaese = "SELECT s.paese, a.sentiment FROM articoli AS a JOIN notizie AS n ON a.link = n.dlink JOIN sitiweb AS s ON n.sitoweb = s.nome WHERE a.emptytext = 0"


print("Raccolta dati sentiment...")
#dbcursor.execute(query_sentiment)
#result_s = dbcursor.fetchall()
dbcursor.execute(query_sentiment_perpaese)
result_sp = dbcursor.fetchall()
#print("Raccolta dati qualità...")
#dbcursor.execute(query_quality)
#result_q = dbcursor.fetchall()


#Chiusura connessione
dbcursor.close()
dbconnection.close()

#------------------------------------------------------------------------------------


print("Preparazione dati...")
#dataset_s = pd.DataFrame(result_s, columns=["Sentiment"])
dataset_sp = pd.DataFrame(result_sp, columns=["Paese","Sentiment"])
print(result_sp)
print(dataset_sp)
#dataset_q = pd.DataFrame(result_q, columns=["Qualità"])

mpl.rcParams['font.size'] = 12.0

'''
grafico = sb.boxplot(x="Sentiment", data=dataset_s)
grafico.axes.set_title("Distribuzione del sentiment",fontsize=25)
grafico.set_xlabel("Sentiment",fontsize=20)
plt.show()
'''
grafico1 = sb.boxplot(x="Sentiment", y="Paese", data=dataset_sp)
grafico1.axes.set_title("Distribuzione sentiment per paese",fontsize=25)
grafico1.set_xlabel("Sentiment",fontsize=20)
grafico1.set_ylabel("Paese",fontsize=20)
plt.show()
'''
grafico2 = sb.boxplot(x="Qualità", data=dataset_q)
grafico2.axes.set_title("Distribuzione della qualità",fontsize=25)
grafico2.set_xlabel("Qualità",fontsize=20)
plt.show()
'''

#Fine script

print("\n---------- ESECUZIONE TERMINATA! ----------")