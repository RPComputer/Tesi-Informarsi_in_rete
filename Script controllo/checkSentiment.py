'''
Nome:


Obiettivo:


Passaggi:
Collegarsi al database
Ottenere il log
Effettuare il grafico con seaborn
Salvare il grafico
'''
import mysql.connector
import numpy as np
import pandas as pd
import matplotlib as mpl
import seaborn as sb
import matplotlib.pyplot as plt
import joblib
import msvcrt as m


def wait():
    m.getch()

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
print("----- Verifica distribuzione sentiment ----\n")

query = "SELECT sentiment FROM articoli"

print("Connessione al database... ")
dbconnection = connect_to_db()
dbcursor = dbconnection.cursor();
print("completata\n")

print("Raccolta del degli articoli interessati...")

dbcursor.execute(query)
result = dbcursor.fetchall()
print("Dumping...")
joblib.dump(result, 'sentiment.pkl')

#---------------------------------------------------------------
#result = joblib.load('sentiment.pkl')
dataset = pd.DataFrame(result, columns=["Sentiment"])

print("Elaborazione grafico...")
grafico = sb.boxplot(x="Sentiment",data=dataset)
'''
for item in grafico.get_xticklabels():
    item.set_rotation(90)
'''

print("Plotting...")
plt.show()

#Chiusura connessione
dbcursor.close()
dbconnection.close()



#Fine script

print("\n---------- ESECUZIONE TERMINATA! ----------")