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
newsconnection = connect_to_db()
newscursor = newsconnection.cursor();
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
	if notizie == ():
		break
	dbconnection = connect_to_db()
	dbcursor = dbconnection.cursor();
	for n in notizie:
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
		#Output di aggiornamento
		progress = progress + 1
		percentage = progress/newsnum*100
		print("Avanzamento: " percentage "   " progress "/" newsnum, end='\r')
	dbcursor.close()
	dbconnection.close()

newscursor.close()
newsconnection.close()


#chiusura script

print("\n---------- ESECUZIONE TERMINATA! ----------")
