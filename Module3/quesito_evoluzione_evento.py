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
import msvcrt as m

import itertools

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
print("------ Elaborazione grafico andamento -----\n")
'''
query = "SELECT npm.giorno, npm.paese, tm.categoria FROM topicMorandi AS tm JOIN notiziePaesiMorandi AS npm ON tm.articolo = npm.link WHERE npm.giorno IS NOT NULL GROUP BY npm.paese, npm.giorno, tm.categoria ORDER BY npm.giorno"

print("Connessione al database... ")
dbconnection = connect_to_db()
dbcursor = dbconnection.cursor();
print("completata\n")

print("Raccolta del degli articoli interessati...")

dbcursor.execute(query)
result = dbcursor.fetchall()
joblib.dump(result, 'rawDatasetPonteMorandi.pkl')

#preparazione dei dati
print("Pulizia dati...")

toremove = []
for i in range(len(insieme_articoli)):
		insieme_articoli[i] = list(insieme_articoli[i])
		if insieme_articoli[i][0] == None:
			toremove.append(insieme_articoli[i])

for i in toremove:
	insieme_articoli.remove(i)


for a in result:
	a = list(a)
	a[0] = a[0].date()
	print(a)

print(len(result))

print("Dumping...")
joblib.dump(result, 'datasetPonteMorandi.pkl')
'''

#---------------------------------------------------------------
#mpl.rcParams['font.size'] = 14.0
print("Caricamento dati...")
result = list(joblib.load('datasetPonteMorandi.pkl'))
print("Preparazione dati...")
'''
for r in result:
	r=list(r)
	temp = str(r[0])
	temp = temp[5:11]
	r[0] = temp
	print(temp, r[0])
'''
dataset = pd.DataFrame(result, columns=["Data","Paese","Categoria"])

print("Elaborazione grafico...")
grafico = sb.swarmplot(x="Data", y="Paese", hue="Categoria", data=dataset)
#grafico.set(xlabel='Data', ylabel='Paesi:')
grafico.axes.set_title("Evoluzione spazio-temporale evento Ponte Morandi",fontsize=25)
grafico.set_xlabel("Data",fontsize=20)
grafico.set_ylabel("Paesi:",fontsize=20)
for item in grafico.get_xticklabels():
    item.set_rotation(90)
'''
xlabels = grafico.get_xticklabels()
for x in xlabels:
	temp = x.get_text()[5:11]
	x.set_text(temp)
grafico.set_xticklabels(xlabels,rotation=90)
'''
print("Plotting...")
plt.show()
'''
#Chiusura connessione
dbcursor.close()
dbconnection.close()
'''


#Fine script

print("\n---------- ESECUZIONE TERMINATA! ----------")