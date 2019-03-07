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

def crea_grafico(dataset, x, y, xlabel, ylabel):
	grafico = sb.lmplot(x=x, y=y, data=dataset)
	grafico.set(xlabel=xlabel, ylabel=ylabel, fontsize = 20)
	ax = plt.gca()
	ax.set
	print("Plotting...")
	plt.show()
	
sb.set(style="darkgrid")

print("Caricamento dati...")

dataset = pd.read_csv("dataset_quesito_2.CSV", sep=';')
print(dataset)

print("Elaborazione grafici...")


crea_grafico(dataset, 'qualita', 'pil', "Qualità", "PIL")
crea_grafico(dataset, 'qualita', 'pilPC', "Qualità", "PIL Pro Capite")
crea_grafico(dataset, 'qualita', 'popolazione', "Qualità", "Popolazione (in miliardi)")
crea_grafico(dataset, 'qualita', 'densita', "Qualità", "Densità di popolazione")
crea_grafico(dataset, 'qualita', 'estensione', "Qualità", "Superficie KM2 (in milioni)")

crea_grafico(dataset, 'notizie', 'pil', "Numero di notizie", "PIL")
crea_grafico(dataset, 'notizie', 'pilPC', "Numero di notizie", "PIL Pro Capite")
crea_grafico(dataset, 'notizie', 'densita', "Numero di notizie", "Densità di popolazione")
crea_grafico(dataset, 'notizie', 'popolazione', "Numero di notizie", "Popolazione (in miliardi)")
crea_grafico(dataset, 'notizie', 'estensione', "Numero di notizie", "Superficie KM2 (in milioni)")

#Fine script

print("\n---------- ESECUZIONE TERMINATA! ----------")