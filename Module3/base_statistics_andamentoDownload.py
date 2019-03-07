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
import joblib
import datetime
import matplotlib.pyplot as plt

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
print("------ Elaborazione grafico andamento -----\n")
'''
print("Connessione al database... ")
dbconnection = connect_to_db()
dbcursor = dbconnection.cursor();
print("completata\n")
'''
print("Raccolta del log...")
#dbcursor.execute("SELECT data FROM log WHERE downloadsuccess = 1")
#log = dbcursor.fetchall()

#joblib.dump(log, 'log.pkl')
log = joblib.load('logDownload.pkl')


log1 = [x[0].date() for x in log]
print("Plotting...")
grafico = sb.countplot(log1, color='blue')
grafico.axes.set_title("Andamento download",fontsize=25)
grafico.set_xlabel("Data",fontsize=20)
grafico.set_ylabel("Numero delle notizie",fontsize=20)
xlabels = grafico.get_xticklabels()
for x in xlabels:
	temp = x.get_text()[5:11]
	x.set_text(temp)

grafico.set_xticklabels(xlabels,rotation=90)
plt.show()

'''
#Chiusura connessione
dbcursor.close()
dbconnection.close()
'''


#Fine script

print("\n---------- ESECUZIONE TERMINATA! ----------")