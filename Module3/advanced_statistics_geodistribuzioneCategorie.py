'''
7 donut plot (uno per paese)
Onuno con le percenutali della categoria sul paese
Esempio: Italia: 27% politica; 30% sport; ecc.. (numeri casuali)

QUERY:
SELECT a.categoria, COUNT(*)
FROM articoli AS a JOIN 
	(SELECT n.dlink, s.paese
	FROM notizie AS n JOIN sitiweb AS s ON n.sitoweb = s.nome
	WHERE s.paese = '') AS sub ON a.link = sub.dlink
WHERE a.categoria IS NOT NULL
GROUP BY a.categoria
'''

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

dataset = []

print("Raccolta delle informazioni...")
dbcursor.execute("SELECT a.categoria, COUNT(*) FROM articoli AS a JOIN (SELECT n.dlink, s.paese FROM notizie AS n JOIN sitiweb AS s ON n.sitoweb = s.nome WHERE s.paese = 'Italia') AS sub ON a.link = sub.dlink WHERE a.categoria IS NOT NULL GROUP BY a.categoria")
c_italia = dbcursor.fetchall()
print("italia")
dbcursor.execute("SELECT a.categoria, COUNT(*) FROM articoli AS a JOIN (SELECT n.dlink, s.paese FROM notizie AS n JOIN sitiweb AS s ON n.sitoweb = s.nome WHERE s.paese = 'USA') AS sub ON a.link = sub.dlink WHERE a.categoria IS NOT NULL GROUP BY a.categoria")
c_usa = dbcursor.fetchall()
print("usa")
dbcursor.execute("SELECT a.categoria, COUNT(*) FROM articoli AS a JOIN (SELECT n.dlink, s.paese FROM notizie AS n JOIN sitiweb AS s ON n.sitoweb = s.nome WHERE s.paese = 'India') AS sub ON a.link = sub.dlink WHERE a.categoria IS NOT NULL GROUP BY a.categoria")
c_india = dbcursor.fetchall()
print("india")
dbcursor.execute("SELECT a.categoria, COUNT(*) FROM articoli AS a JOIN (SELECT n.dlink, s.paese FROM notizie AS n JOIN sitiweb AS s ON n.sitoweb = s.nome WHERE s.paese = 'UK') AS sub ON a.link = sub.dlink WHERE a.categoria IS NOT NULL GROUP BY a.categoria")
c_uk = dbcursor.fetchall()
print("uk")
dbcursor.execute("SELECT a.categoria, COUNT(*) FROM articoli AS a JOIN (SELECT n.dlink, s.paese FROM notizie AS n JOIN sitiweb AS s ON n.sitoweb = s.nome WHERE s.paese = 'Australia') AS sub ON a.link = sub.dlink WHERE a.categoria IS NOT NULL GROUP BY a.categoria")
c_australia = dbcursor.fetchall()
print("australia")
dbcursor.execute("SELECT a.categoria, COUNT(*) FROM articoli AS a JOIN (SELECT n.dlink, s.paese FROM notizie AS n JOIN sitiweb AS s ON n.sitoweb = s.nome WHERE s.paese = 'Canada') AS sub ON a.link = sub.dlink WHERE a.categoria IS NOT NULL GROUP BY a.categoria")
c_canada = dbcursor.fetchall()
print("canada")
dbcursor.execute("SELECT a.categoria, COUNT(*) FROM articoli AS a JOIN (SELECT n.dlink, s.paese FROM notizie AS n JOIN sitiweb AS s ON n.sitoweb = s.nome WHERE s.paese = 'Sudafrica') AS sub ON a.link = sub.dlink WHERE a.categoria IS NOT NULL GROUP BY a.categoria")
c_sudafrica = dbcursor.fetchall()
print("sud africa")

dataset.append(c_italia)
dataset.append(c_usa)
dataset.append(c_india)
dataset.append(c_uk)
dataset.append(c_australia)
dataset.append(c_sudafrica)
dataset.append(c_canada)

print("Dumping dataset...")
joblib.dump(dataset, 'datasetDistGeog.pkl')
'''
dataset = joblib.load('datasetDistGeog.pkl')
nomi_paesi = ["Italia","USA","India","UK","Australia","Sudafrica","Canada"]
mpl.rcParams['font.size'] = 14.0

for i in range(len(dataset)):
	categorie, n = zip(*dataset[i])
	categorie = list(categorie)
	n = list(n)
	categorie.reverse()
	n.reverse()
	for j in range(len(categorie)):
		categorie[j] = categorie[j].capitalize()
	
	
	fig, ax = plt.subplots()
	ax = fig.add_subplot(111)
	cerchio = plt.Circle((0,0), 0.7, color='white')
	x = 0
	y = 0
	ax.add_patch(cerchio)
	label = ax.annotate(nomi_paesi[i], xy=(x, y), fontsize=25, ha="center")
	ax.set_aspect('equal')
	ax.autoscale_view()
	grafico = plt.pie(n, labels=categorie, colors=sb.color_palette('muted'))
	p = plt.gcf()
	p.gca().add_artist(cerchio)	
	plt.show()


'''
#Chiusura connessione
dbcursor.close()
dbconnection.close()
'''


#Fine script

print("\n---------- ESECUZIONE TERMINATA! ----------")