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
def wait():
    m.getch()

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
print("------ Elaborazione grafico andamento -----\n")

'''
print("Connessione al database... ")
dbconnection = connect_to_db()
dbcursor = dbconnection.cursor();
print("completata\n")

print("Raccolta del log...")

#---------------------------------------------------------------

dbcursor.execute("SELECT l.data, a.categoria FROM log AS l JOIN articoli AS a ON l.notizia = a.link WHERE downloadsuccess = 1 AND categoria = 'altro'")
log_altro = dbcursor.fetchall()
print("altro")
dbcursor.execute("SELECT l.data, a.categoria FROM log AS l JOIN articoli AS a ON l.notizia = a.link WHERE downloadsuccess = 1 AND categoria = 'cronaca'")
log_cronaca = dbcursor.fetchall()
print("cronaca")
dbcursor.execute("SELECT l.data, a.categoria FROM log AS l JOIN articoli AS a ON l.notizia = a.link WHERE downloadsuccess = 1 AND categoria = 'cultura e intrattenimento'")
log_cei = dbcursor.fetchall()
print("cultura e intrattenimento")
dbcursor.execute("SELECT l.data, a.categoria FROM log AS l JOIN articoli AS a ON l.notizia = a.link WHERE downloadsuccess = 1 AND categoria = 'economia'")
log_economia = dbcursor.fetchall()
print("economia")
dbcursor.execute("SELECT l.data, a.categoria FROM log AS l JOIN articoli AS a ON l.notizia = a.link WHERE downloadsuccess = 1 AND categoria = 'esteri'")
log_esteri = dbcursor.fetchall()
print("esteri")
dbcursor.execute("SELECT l.data, a.categoria FROM log AS l JOIN articoli AS a ON l.notizia = a.link WHERE downloadsuccess = 1 AND categoria = 'politica'")
log_politica = dbcursor.fetchall()
print("politica")
dbcursor.execute("SELECT l.data, a.categoria FROM log AS l JOIN articoli AS a ON l.notizia = a.link WHERE downloadsuccess = 1 AND categoria = 'salute e benessere'")
log_seb = dbcursor.fetchall()
print("salute e benessere")
dbcursor.execute("SELECT l.data, a.categoria FROM log AS l JOIN articoli AS a ON l.notizia = a.link WHERE downloadsuccess = 1 AND categoria = 'scienza e tecnologia'")
log_set = dbcursor.fetchall()
print("scienza e tecnologia")
dbcursor.execute("SELECT l.data, a.categoria FROM log AS l JOIN articoli AS a ON l.notizia = a.link WHERE downloadsuccess = 1 AND categoria = 'sport'")
log_sport = dbcursor.fetchall()
print("sport")


log=[]
log.append(log_altro)
log.append(log_cronaca)
log.append(log_cei)
log.append(log_economia)
log.append(log_esteri)
log.append(log_politica)
log.append(log_seb)
log.append(log_set)
log.append(log_sport)

joblib.dump(log, 'logCategorie.pkl')
'''
log = joblib.load('logCategorie.pkl')

#---------------------------------------------------------------
print("Premere un tasso per continuare")
wait()

for l in log:
	for i in range(len(l)):
		l[i] = list(l[i])


for l in log:
	for d in l:
		d[0] = d[0].date()

for l in log:
	print("Elaborazione " + l[0][1] + " ...")
	dataset = [x for (x,y) in l]
	grafico = sb.countplot(dataset, color='blue')
	grafico.axes.set_title("Andamento: "+l[0][1],fontsize=25)
	grafico.set_xlabel("Data",fontsize=20)
	grafico.set_ylabel('Numero delle notizie',fontsize=20)
	xlabels = grafico.get_xticklabels()
	for x in xlabels:
		temp = x.get_text()[5:11]
		x.set_text(temp)
	grafico.set_xticklabels(xlabels,rotation=90)
	print("Plotting...")
	plt.ylim(0,4000)
	plt.show()
'''
#Chiusura connessione
dbcursor.close()
dbconnection.close()
'''


#Fine script

print("\n---------- ESECUZIONE TERMINATA! ----------")