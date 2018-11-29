'''
Nome:
Estrattore degli articoli

Obiettivo:
Estrarre dal codice HTML delle notizie gli articoli

Passaggi:
Collegarsi al database
Ottenere la lista delle notizie
Per ogni notizia estrarre il testo ed il titolo con newspaper e salvare il testo puro
Per ogni operazione completata dare output per seguire il programma in forma numerica/percentuale
'''

import mysql.connector
from newspaper import Article
import sys

#Funzione di connessione al database
def connect_to_db():
	try:
		res = mysql.connector.connect(user='module1', password='insertnews', host='localhost', database='tesi', charset="utf8", use_unicode=True)
		return res
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("\nPassword e/o username errati")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("\nDatabase does not exist")
		else:
			print("\nErrore: " + err)
		return None

#Inizio script
print("---------- MODULO 2 - ESECUZIONE ----------\n")
print("-------- Estrazione testo articoli---------\n")
print("Connessione al database... ")
newsconnection = connect_to_db()
newscursor = newsconnection.cursor();
print("completata\n")

#Caricamento ed inizializzazione delle variabili globali
newsnum = 386598
ce = 0
newscursor.execute("SELECT link FROM articoli")
elencoarticoli = newscursor.fetchall()
progress = 0 + len(elencoarticoli)

#Caricamento pagine HTML non ancora processate
print("Raccolta pagine html...\n")
newscursor.execute("SELECT * FROM notizie WHERE dlink NOT IN (SELECT link FROM articoli)")

print("Notizie ottenute\n")

rm = "read more"
Rm = "Read more"
RM = "Read More"

print("Estrazione articoli...\n")

while True:
	fetcherror = 0
	#Caricamento di 200 notizie per volta al fine di non occupare troppa RAM, gestione degli errori per riconnessione
	try:
		notizie = newscursor.fetchmany(200)
	except:
		e = sys.exc_info()[0]
		fetcherror = 1
		ce = ce + 1
		print(e)
	if fetcherror == 0:
		#Interruzione del ciclo while quando la raccolta di nuove notizie da un insieme vuoto
		if notizie == ():
			break
		#Nuova connessione per getire il salvataggio dei dati sul database
		dbconnection = connect_to_db()
		dbcursor = dbconnection.cursor();
		#Per ogni notizia dell'insieme raccolto eseguire l'estrazione dell'articolo
		for n in notizie:
			#if (n[0],) not in elencoarticoli:
			#Estrazione info dall'articolo
			html = n[4]
			#Controllo per evitare errori che il codice HTML sia effettivamente presente
			if len(html) > 1:
				#Dichiarazione di un nuovo articolo (oggetto della libreria newspaper) e assegnamento del codice all'oggetto
				a = Article('')
				a.set_html(html)
				a.parse()
				#Acquisizione informazioni
				title = a.title
				text = a.text
				completetext = title + text
				voidTitleArticle = 0
				voidTextArticle = 0
				readmore = 0

				#Controllo lunghezza del titolo
				titleArticleLen = len(title.split())
				#Se è vuoto viene contato
				if titleArticleLen == 0:
					voidTitleArticle = 1
				#Controllo lunghezza del testo
				textArticleLen = len(text.split())
				#Se è vuoto viene contato
				if textArticleLen == 0:
					voidTextArticle = 1
				lunghezzaTesto = len(completetext.split())

				#Controllo presenza read more
				if text.find(rm, (len(text)-200), len(text)) >= 0:
					readmore = 1
				if text.find(Rm, (len(text)-200), len(text)) >= 0:
					readmore = 1
				if text.find(RM, (len(text)-200), len(text)) >= 0:
					readmore = 1
			else:
				completetext = ""
				lunghezzaTesto = 0
				voidTitleArticle = 1
				voidTextArticle = 1
				readmore = 0
				ce = ce + 1
			#Inserimento delle informazioni nel database
			extracted_article = ("INSERT INTO articoli (link, testo, lunghezza, emptytitle, emptytext, rm_flag) VALUES (%s, %s, %s, %s, %s, %s)")
			extracted_data = (n[0], completetext, lunghezzaTesto, voidTitleArticle, voidTextArticle, readmore)
			dbcursor.execute(extracted_article, extracted_data)
			dbconnection.commit()
			
			#Output di aggiornamento
			progress = progress + 1
			percentage = progress/newsnum*100
			print("Avanzamento: ",  progress, "/", newsnum, "\t- %0.3f" % percentage, "%\t<>  Errori: ", ce, end='\r')
		dbcursor.close()
		dbconnection.close()

print("Elaborazione completata di: ", progress, " notizie")

#Chiusura connessione principale
newscursor.close()
newsconnection.close()


#Fine script

print("\n---------- ESECUZIONE TERMINATA! ----------")
