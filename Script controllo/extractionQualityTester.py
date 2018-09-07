import mysql.connector
import os
from newspaper import Article

'''
Collegarsi al database
Ottenere la lista delle notizie
Per ogni notizia estrarre il testo ed il titolo e salvare il testo puro
Per ogni operazione completata dare output per seguire il programma in forma numerica/percentuale
'''

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

#connessione al database
print("---------- MODULO 2 - ESECUZIONE ----------\n")
print("-------- Test estrazione testo articoli---------\n")
print("Connessione al database... ")
newsconnection = connect_to_db()
newscursor = newsconnection.cursor()
print("completata\n")
newscursor.execute("SELECT COUNT * FROM notizie")
newsnum = newscursor.fetchall()
progress = 0

#raccolta link siti web
print("Raccolta pagine html...\n")
newscursor.execute("SELECT * FROM notizie")

print("Notizie ottenute\n")



print("Estrazione articoli...\n")

while True:
	notizie = newscursor.fetchmany(50)
	if testate == 10000:
		break
	for n in notizie:
		#Estrazione info dall'articolo
		html = n.notizia
		a = Article('')
		a.set_html(html)
		a.parse()
		titleArticle = a.title
		textArticle = a.text
		
		#Conteggio numero aticoli testati
		testate++
		
		#Controllo lunghezza titolo
		titleArticleLen = len(titleArticle.split())
		
		#Se è vuoto lo conta
		if titleArticleLen == 0:
			voidTitleArticle++
			errAttuale = True
		
		#Controllo lunghezza testo
		textArticleLen = len(textArticle.split())
		
		#Se è vuoto o corto lo conta
		if textArticleLen == 0:
			voidTextArticle++
			errAttuale = True
		elif textArticleLen <= 20:
			textArticleShort++
			errAttuale = True
		
		#Controllo presenza read more
		if textArticle.find("read more", beg=len(textArticle)-10, end=len(textArticle)) >= 0:
			readMore = True
			errAttuale = True
		if textArticle.find("Read more", beg=len(textArticle)-10, end=len(textArticle)) >= 0:
			readMore = True
			errAttuale = True
		
		#Se ha trovato un read more lo conta
		if readMore:
			RMcount++
			readMore = False
		
		#Se questo articolo è vuoto, corto o contiene un read more lo conta
		if errAttuale:
			errori++
			errAttuale = False
		
		#Output di aggiornamento
		print("Avanzamento:   Testate: " testate "   Errori" errori, end='\r')
		
		#Conteggio lunghezza totale
		TOTtextLen = TOTtextLen + textArticleLen
		
	percErrori = errori*100 / testate
	lunghezzaMedia = TOTtextLen / testate
	os.system("PAUSE")
	os.system("cls")
	print(">>>>>>>> RISULTATI FINALI ANALISI <<<<<<<< \n\n")
	print("Titoli vuoti: " voidTitleArticle "\n")
	print("Articoli vuoti: " voidTextArticle "\n")
	print("Read more trovati: " RMcount "\n")
	print("Errori trovati: " errori "\n")
	print("Percentuale errori trovati: " percErrori "\n")
	print("Lunghezza media articoli: " lunghezzaMedia "\n")
newscursor.close()
newsconnection.close()


#chiusura script

print("\n---------- ESECUZIONE TERMINATA! ----------")
