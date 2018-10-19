from textblob import TextBlob
import nltk
#nltk.download('wordnet')
#nltk.download('brown')
#nltk.download('punkt')

text = TextBlob("Oggi e domani il commissario europeo agli Affari economici, Pierre Moscovici, ? impegnato a Roma in una serie di incontri mentre il confronto dell'Italia con l'Ue sulla manovra entra nel vivo. L'appuntamento chiave ? nel pomeriggio di oggi con il ministro dell'Economia, Giovanni Tria, al termine del quale si svolger? un punto stampa allo stesso ministero.  Moscovici dar? a Tria lettera con richiesta di chiarimenti Il commissario europeo agli Affari economici consegner? direttamente al ministro dell'Economia, Giovanni Tria, una lettera con richieste di chiarimenti dell'esecutivo comunitario sul piano di Bilancio notificato dall'Italia. Lo riporta France Presse citando 'fonti europee'. Al termine del faccia a faccia al ministero di Via XX Settembre, ? prevista nel tardo pomeriggio una conferenza congiunta Tria-Moscovici.  Incontri con Mattarella e Visco Moscovici vedr? anche il governatore della Banca d'Italia, Ignazio Visco, e si recher? in visita di cortesia al Quirinale, dal presidente della Repubblica Sergio Mattarella.  L'esponente della commissione parteciper? infine a un convegno a porte chiuse organizzato da Aspen Institute Italia e Institut Aspen France. Al termine delle visite romane, incontrer? nuovamente i giornalisti presso la rappresentanza in Italia della Commissione, venerd? pomeriggio. Conte: 'Manovra molto bella' 'Personalmente, pi? passa il tempo pi? mi convinco che la manovra ? molto bella'. Lo afferma il presidente del Consiglio, Giuseppe Conte, a margine dei lavori del Consiglio europeo, a Bruxelles. 'Con Juncker mi vedr? presto. Mi rendo perfettamente conto che non ? questa la manovra che si aspettavano alla Commissione, ? comprensibile che ci siano delle reazioni, ci aspettavamo delle osservazioni critiche', prosegue il premier.")
nomi = text.noun_phrases
#print(text.detect_language())

#poichè in italiano la ricerca dei nomi funziona molto peggio rispetto all'inglese effettuo la traduzione, il risultato più affidabile
translated = text.translate(to="en")
names2 = translated.noun_phrases #ottengo la lista dei topic
print(names2)
print("Tutti: ", len(names2))
print("_____________________________________________________")
'''
entext = TextBlob("The Washington Post has published what the newspaper describes as the 'last piece' written by missing Saudi journalist Jamal Khashoggi, who was allegedly killed and dismembered in his country's consulate in Istanbul earlier this month. In a note at the top of the column, published late Wednesday, Post Global Opinions editor Karen Attiah wrote that she 'held off publishing it because we hoped Jamal would come back to us.''Now I have to accept: That is not going to happen,' she said. 'This is the last piece of his I will edit for The Post. This column perfectly captures his commitment and passion for freedom in the Arab world. A freedom he apparently gave his life for.'")
names = entext.noun_phrases
print(entext.detect_language())
'''

'''
for n in nomi:
	if len(n) < 20:
		print(n)
print("_____________________________________________________")
'''
tags = []

rdup = list(set(names2)) #rimozione duplicati puri

def contains_word(s, w):
	return(' ' + w + ' ') in (' ' + s + ' ')

def diff(first, second):
	f = first.copy()
	s = second.copy()
	for i in s:
		f.remove(i)
	return f

print(rdup)
print("Senza duplicati: ", len(rdup))
rimossi = diff(names2, rdup)
print("Rimossi: ", rimossi)
print("Numero rimossi: ", len(rimossi))
print("_____________________________________________________")


atmp = []

#nel for effettuo la rimozione dei dublicati logici: es. sergio mattarella e mattarella sono la stessa cosa, viene mantenuto solo sergio mattarella
for t in rdup:
	f = True
	atmp = rdup.copy()
	atmp.remove(t)
	for a in atmp:
		if contains_word(a, t):
			f = False
			print(a, " | ", t)
	if f:
		tags.append(t)

print(tags)
print("Numero di tags: ", len(tags))
rimossi2 = diff(rdup, tags)
print("Differenza tra risultato e senza duplicati: ", rimossi2)
print("Numero topic logici duplicati rimossi: ", len(rimossi2))
print("_____________________________________________________")
		
'''
for n in names:
	if len(n) < 20:
		print(n)
'''
