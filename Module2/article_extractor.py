import mysql.connector
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
print("-------- Estrazione testo articoli---------\n")
print("Connessione al database... ")
dbconnection = connect_to_db()
print("completata\n")

#raccolta link siti web
print("Raccolta pagine html...\n")
dbcursor = dbconnection.cursor();
dbcursor.execute("SELECT * FROM notizie")
notizie = dbcursor.fetchall()
print("Notizie ottenute\n")
dbcursor.close()
dbconnection.close()

newsnum = len(notizie)
progress = 0

print("Estrazione articoli...\n")
for n in notizie:
	dbconnection = connect_to_db()
	dbcursor = dbconnection.cursor();
	#Se le informazioni non sono state estratte eseguo altrimenti passo alla prossima
	if n.title == None:
		#Estrazione info dall'articolo
		html = n.notizia
		a = Article('')
		a.set_html(html)
		a.parse()
		title = a.title
		text = a.text
		#Inserimento delle informazioni nel database
		update_news = ("UPDATE notizie SET (titolo, testo) VALUES (%s, %s) WHERE dlink VALUES (%s)")
		update_data = (title, text, n.dlink)
		dbcursor.execute(update_news, update_data)
		dbconnection.commit()
	dbcursor.close()
	dbconnection.close()
	#Output di aggiornamento
	progress = progress + 1
	percentage = progress/newsnum*100
	print("Avanzamento: " percentage "   " progress "/" newsnum, end='\r')



#chiusura script

print("\n---------- ESECUZIONE TERMINATA! ----------")
