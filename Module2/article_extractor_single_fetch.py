import mysql.connector
from newspaper import Article
import sys

'''
Collegarsi al database
Ottenere la lista delle notizie
Per ogni notizia estrarre il testo ed il titolo e salvare il testo puro
Per ogni operazione completata dare output per seguire il programma in forma numerica/percentuale
'''

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

#connessione al database
print("---------- MODULO 2 - ESECUZIONE ----------\n")
print("-------- Estrazione testo articoli---------\n")
print("Connessione al database... ")
newsconnection = connect_to_db()
newscursor = newsconnection.cursor();
print("completata\n")
newsnum = 386598
ce = 0
newscursor.execute("SELECT link FROM articoli")
elencoarticoli = newscursor.fetchall()
progress = 0 + len(elencoarticoli)

#raccolta link siti web
print("Raccolta pagine html...\n")
newscursor.execute("SELECT * FROM notizie WHERE dlink NOT IN (SELECT link FROM articoli)")

print("Notizie ottenute\n")

rm = "read more"
Rm = "Read more"
RM = "Read More"

print("Estrazione articoli...\n")

while True:
	fetcherror = 0
	try:
		notizie = newscursor.fetchone()
	except:
		e = sys.exc_info()[0]
		fetcherror = 1
		ce = ce + 1
		print(e)
	if fetcherror == 0:
		if notizie == ():
			break
		dbconnection = connect_to_db()
		dbcursor = dbconnection.cursor();
		#Estrazione info dall'articolo
		html = notizie[4]
		if len(html) > 1:
			a = Article('')
			a.set_html(html)
			a.parse()

			title = a.title
			text = a.text
			completetext = title + text
			voidTitleArticle = 0
			voidTextArticle = 0
			readmore = 0

			#Controllo lunghezza titolo
			titleArticleLen = len(title.split())
			#Se è vuoto lo conta
			if titleArticleLen == 0:
				voidTitleArticle = 1
			#Controllo lunghezza testo
			textArticleLen = len(text.split())
			#Se è vuoto o corto lo conta
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
		extracted_data = (notizie[0], completetext, lunghezzaTesto, voidTitleArticle, voidTextArticle, readmore)
		dbcursor.execute(extracted_article, extracted_data)
		dbconnection.commit()
		
		#Output di aggiornamento
		progress = progress + 1
		percentage = progress/newsnum*100
		print("Avanzamento: ",  progress, "/", newsnum, "\t- %0.3f" % percentage, "%\t<>  Errori: ", ce, end='\r')
		dbcursor.close()
		dbconnection.close()

print("Elaborazione completata di: ", progress, " notizie")

newscursor.close()
newsconnection.close()


#chiusura script

print("\n---------- ESECUZIONE TERMINATA! ----------")
