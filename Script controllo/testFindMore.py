'''
Nome:
Controllo presenza read more

Obiettivo:
L'algoritmo controlla se è presente la scritta "read more" alla fine del testo dato in input

Passaggi:
Ricerca del read more
Stampa su schermo:
	True	se è presente il read more alla fine del testo
	False	altimenti
'''


#Inizio script

#Testo in input
textArticle = "(CNN)Brexit is a bit like a screaming child. Those of us in the UK want everyone else to care about it as much as we do. But for most European Union member states, it's an annoyance to be gotten rid of -- respectfully, but as quickly as possible. There's no doubt foreign audiences are interested in the process. It is unprecedented, after all. Diplomats from across Europe -- and elsewhere -- are trying to figure out what Brexit will mean, but mostly in terms of what kind of UK will come out of Brexit rather than what kind of EU. Its official -- a no-deal Brexit will make traveling a pain It's official -- a no-deal Brexit will make traveling a pain This much is also clear in the media coverage of Brexit in the EU. Research by the Reuters Institute showed that nearly 60% of Brexit coverage has presented it as a UK-only problem rather than something with big implications for other member states or the EU more widely. And this figure rises to nearly 70% when Irish media is excluded. This is partly because the economic risks from Brexit for most EU member states are seen as negligible and certainly manageable. Academic work suggests about 12% of the UK economy is at risk from Brexit, whereas the EU average is more like 2.5%. Read more"

#Parola o frase da cercare
RM = "Read more"
readMore = False

#Se il read more viene trovato alla fine del testo, setta la variabile readMore a True, altrimenti la lascia a False
if textArticle.find(RM, (len(textArticle)-10), len(textArticle)) >= 0:
	readMore = True

	#Stampa su schermo del risultato
print(readMore)

#Fine script