'''
Nome:
Tester dell'elaborazione del sentiment

Obiettivo:
Utilizzando TextBlob viene testata l'elaborazione del sentiment di un testo

Passaggi:
'''


from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import nltk

#Inizio script
print("AVVIO SCRIPT")
a = "Oggi e domani il commissario europeo agli Affari economici, Pierre Moscovici, ? impegnato a Roma in una serie di incontri mentre il confronto dell'Italia con l'Ue sulla manovra entra nel vivo. L'appuntamento chiave ? nel pomeriggio di oggi con il ministro dell'Economia, Giovanni Tria, al termine del quale si svolger? un punto stampa allo stesso ministero.  Moscovici dar? a Tria lettera con richiesta di chiarimenti Il commissario europeo agli Affari economici consegner? direttamente al ministro dell'Economia, Giovanni Tria, una lettera con richieste di chiarimenti dell'esecutivo comunitario sul piano di Bilancio notificato dall'Italia. Lo riporta France Presse citando 'fonti europee'. Al termine del faccia a faccia al ministero di Via XX Settembre, ? prevista nel tardo pomeriggio una conferenza congiunta Tria-Moscovici.  Incontri con Mattarella e Visco Moscovici vedr? anche il governatore della Banca d'Italia, Ignazio Visco, e si recher? in visita di cortesia al Quirinale, dal presidente della Repubblica Sergio Mattarella.  L'esponente della commissione parteciper? infine a un convegno a porte chiuse organizzato da Aspen Institute Italia e Institut Aspen France. Al termine delle visite romane, incontrer? nuovamente i giornalisti presso la rappresentanza in Italia della Commissione, venerd? pomeriggio. Conte: 'Manovra molto bella' 'Personalmente, pi? passa il tempo pi? mi convinco che la manovra ? molto bella'. Lo afferma il presidente del Consiglio, Giuseppe Conte, a margine dei lavori del Consiglio europeo, a Bruxelles. 'Con Juncker mi vedr? presto. Mi rendo perfettamente conto che non ? questa la manovra che si aspettavano alla Commissione, ? comprensibile che ci siano delle reazioni, ci aspettavamo delle osservazioni critiche', prosegue il premier."
a2 = "Consegna analisi costi-benefici Tav e Venezuela sul tavolo del vertice a Palazzo Chigi Sul clima dell'incontro pesano le tensioni nel governo dopo i risultati del voto in Abruzzo.  Torino-Lione, i 5 Stelle sarebbero decisi per il no. Salvini: non ho ancora letto il dossier. I dossier internazionali e la Tav Torinio-Lione sono al centro del vertice in corso  Palazzo Chigi: dal Venezuela, alle tensioni con la Francia, si fa il punto a poche ore dall'intervento del ministro Enzo Moavero Milanesi alle Camere e del discorso a Strasburgo del presidente del Consiglio Giuseppe Conte. La riunione si sarebbe dovuta tenere ieri sera ma sarebbe stato un ritardo di Conte, rientrato solo intorno alle 23 dalla visita in Sardegna, a portare alla scelta del rinvio. Tav, Salvini: non ho ancora letto il dossier 'Non ho ancora letto il dossier'. Così il vicepremier e ministro dell'Interno, Matteo Salvini, arrivando a Palazzo Chigi, risponde ai cronisti se avesse già letto l'analisi costi-benefici sulla Tav.  Pesa il voto in Abruzzo Sul clima dell'incontro pesano le tensioni nel governo dopo i risultati del voto in Abruzzo. Il vertice è l'occasione - spiegano da M5s e Lega - per chiarirsi e decidere come andare avanti su tanti temi. Al tavolo sono previsti il premier Conte, i vicepremier Luigi Di Maio e Matteo Salvini, i ministri Moavero e Riccardo Fraccaro, e il sottosegretario Giancarlo Giorgetti. Le divergenze sulla crisi in Venezuela In cima all'agenda balza la politica estera, sia perché nel pomeriggio Conte parlerà a Strasburgo, sia per la necessità di raggiungere una posizione comune in Parlamento sul Venezuela: dopo la relazione di Moavero dovrebbe essere messa ai voti una mozione di maggioranza su cui però manca il sigillo politico e l'intesa finale tra M5s e Lega.  Il duello sulla Tav La settimana però è decisiva anche per altri temi delicati: dagli emendamenti al 'decretone', all'intesa sull'autonomia regionale (prevista in Cdm venerdì, potrebbe slittare), fino alla Tav. Ieri sera Danilo Toninelli ha consegnato a Palazzo Chigi l'analisi sui costi-benefici dell'opera ma è sul terreno politico che si cerca un accordo: Di Maio vorrebbe prendere subito una posizione per il no, mentre Salvini - rafforzato dal voto in Abruzzo - preme per il sì e alla fine la soluzione potrebbe essere un rinvio a dopo le europee"
a3 = """
It's not just Mexico that isn't paying for the wall. Congress isn't either, apparently. But President Donald Trump isn't ready to break it to his supporters just yet. Rather than selling a potential breakthrough, reached on Capitol Hill to stave off a new partial government shutdown, Trump revived the molten rhetoric on immigration that helped make him President at a boisterous campaign rally in El Paso, Texas, on Monday night. The drama provided an eloquent snapshot of the political forces over immigration tearing at the cohesion of the Republican Party. Down by the border, Trump was in outsized form, firing off his dubious claims on immigration while torching Democrats with fierce new attacks on climate change and abortion. In Washington, under the Capitol dome, Republican lawmakers worked diligently with those same Democrats on the kind of institutional Washington compromise that anchors the conventional politics Trump disdains. It was not clear what will happen next. But with Trump reveling in the embrace of his adoring, partisan crowd, it's quite possible that he returned to the White House with his base-baiting instincts replenished. In his hour-and-15-minute address, Trump excoriated Democrats and repeated false claims that the nearby wall had meant huge cuts in the city's violent crime. But the President told the audience he had chosen not to learn the details of a bipartisan deal to avert a shutdown before he clambered onstage. If he actually did know full well what was going on, then he couldn't bring himself to describe what on paper appears to be a huge disappointment. That in itself was a hint that there was no famous victory to crow about and that the agreement reached in Washington -- which contains only $1.375 billion for barriers and no wall -- falls well short of the President's demands for $5.7 billion to fund a campaign promise that has an almost mystical hold on his base. He might have dodged the question on Monday night -- but Washington is waiting for an answer. What will the President do next? Will he tear up the congressional agreement and stand with his most loyal supporters by refusing to cave on the wall? Or will he accept the compromise,which could prevent a repeat of a government shutdown that hurt him politically? He seems to be keeping his options open. To embrace the agreement reached in tortuous congressional negotiations, Trump would have to try to spin a clear loss as a win -- a tactic he seemed to hint at during his rally. As his crowd belted out "Build the wall" -- Trump tried to grope for a way out: "You really mean 'finish that wall,' because we have built a lot of it." The President said he had been told by aides before the rally that a deal had been clinched but he had not wanted the crowd kept waiting by finding out what was in it. "I could have stayed out there and listened or I could have come out there to the people of El Paso in Texas. I chose you," Trump said. "Maybe progress has been made, maybe not." But details were already filtering out of the talks in Washington about the shape of Monday's deal. It is hard to believe that the President wouldn't have been told if the outcome had matched his demands that triggered the longest government shutdown in history late last year. He also declined to go into details on the deal in an interview with conservative Fox News pundit Laura Ingraham, who has a proven track record of influencing him on immigration matters -- conducted before his rally. "A lot of things have changed. I can't go into detail -- I just heard it very quickly coming over to see you," Trump told Ingraham. Emphasizing the scale of his dilemma, his conservative allies in the House began to mobilize against the deal. "While the President was giving a great speech in El Paso, Congress was putting together a bad deal on immigration," tweeted House Freedom Caucus co-founder Rep. Jim Jordan, an Ohio Republican.
"""

a4 = """
The quick and easy noshes you love are chipping away at your mortality one nibble at a time, according to new research from France: We face a 14% higher risk of early death with each 10% increase in the amount of ultraprocessed foods we eat.
"Ultraprocessed foods are manufactured industrially from multiple ingredients that usually include additives used for technological and/or cosmetic purposes," wrote the authors of the study, published Monday in the journal JAMA Internal Medicine. "Ultraprocessed foods are mostly consumed in the form of snacks, desserts, or ready-to-eat or -heat meals," and their consumption "has largely increased during the past several decades."
This trend may drive an increase of early deaths due to chronic illnesses, including cancer and cardiovascular disease, they say. In the United States, 61% of an adult's total diet comes from ultraprocessed foods, in Canada, it is 62%, and in the UK, that proportion is 63%, a recent study found. Yet research also indicates that eating ultraprocessed foods can lead to obesity, high blood pressure and cancer, the study authors say. To understand the relationship between ultraprocessed foods and the risk of an earlier-than-expected death, the researchers enlisted the help of 44,551 French adults 45 and older for two years. Their average age was 57, and nearly 73% of the participants were women. All provided 24-hour dietary records every six months in addition to completing questionnaires about their health (including body-mass index and other measurements), physical activities and sociodemographics.
The researchers calculated each participant's overall dietary intake and consumption of ultraprocessed foods.
Ultraprocessed foods accounted for more than 14% of the weight of total food consumed and about 29% of total calories, they found. Ultraprocessed food consumption was associated with younger age, lower income, lower educational level, living alone, higher BMI and lower physical activity level. Over the study period, 602 participants died. After adjusting for factors such as smoking, the researchers calculated an associated 14% higher risk of early death for each 10% increase in the proportion of ultraprocessed foods consumed.
Further studies are needed to confirm these results, the authors say. Still, they speculate that the additives, the packaging (chemicals leech into the food during storage) and the processing itself, including high-temperature processing, may be the factors that negatively affect health.
"""

a5 = """
How listening to music helps your brain
MELBOURNE, AUSTRALIA - NOVEMBER 01:  Race goes enjoy the atmosphere during The Melbourne Cup at Flemington Racecourse November 1, 2005 in Melbourne, Australia.  (Photo by Kristian Dowling/Getty Images)
Saying this word can extend your life
MUNICH, GERMANY - JULY 09:  FC Bayern Muenchen sporting manager Matthias Sammer laughs during a press conference at the Bayern Muenchen training ground on July 9, 2014 in Munich, Germany.  (Photo by Alexandra Beier/Bongarts/Getty Images)
Does laughing make you healthier?
A fruit plate is seen at the Buchinger-Wilhelmi Clinic in Ueberlingen, southern Germany, on March 24, 2014. High-end clinics specialising in deprivation rather than pampering are all the rage in Germany, one of the homes of the fasting movement, and in some cases it is even covered by health insurance plans. AFP PHOTO/CHRISTOF STACHE        (Photo credit should read CHRISTOF STACHE/AFP/Getty Images)
The best diets have this in common
How to stop mindless eating
Beautiful girl sleeps in the bedroom, lying on bed, isolated
To get good sleep, set thermostat at this
Do this at 50 and you could live to 100
Trick your kids into eating healthy
Get outside to improve your health
This string may help you live to be 100
Is sitting the new smoking?
Put down that energy drink!
Cut this food and extend your life
Meditation has become increasingly popular in the West since the 1960s. 
How every person can benefit from meditation
wine glasses
Drink this daily and you may live longer
How listening to music helps your brain
MELBOURNE, AUSTRALIA - NOVEMBER 01:  Race goes enjoy the atmosphere during The Melbourne Cup at Flemington Racecourse November 1, 2005 in Melbourne, Australia.  (Photo by Kristian Dowling/Getty Images)
Saying this word can extend your life
MUNICH, GERMANY - JULY 09:  FC Bayern Muenchen sporting manager Matthias Sammer laughs during a press conference at the Bayern Muenchen training ground on July 9, 2014 in Munich, Germany.  (Photo by Alexandra Beier/Bongarts/Getty Images)
Does laughing make you healthier?
A fruit plate is seen at the Buchinger-Wilhelmi Clinic in Ueberlingen, southern Germany, on March 24, 2014. High-end clinics specialising in deprivation rather than pampering are all the rage in Germany, one of the homes of the fasting movement, and in some cases it is even covered by health insurance plans. AFP PHOTO/CHRISTOF STACHE        (Photo credit should read CHRISTOF STACHE/AFP/Getty Images)
The best diets have this in common
How to stop mindless eating
Beautiful girl sleeps in the bedroom, lying on bed, isolated
To get good sleep, set thermostat at this
Do this at 50 and you could live to 100
Trick your kids into eating healthy
Get outside to improve your health
This string may help you live to be 100
Is sitting the new smoking?
Put down that energy drink!
Cut this food and extend your life
Meditation has become increasingly popular in the West since the 1960s. 
How every person can benefit from meditation
wine glasses
Drink this daily and you may live longer
How listening to music helps your brain
It takes moxie to flip an unhealthy lifestyle to a healthy one -- particularly for folks over 60.
Most baby boomers approach retirement age unwilling to follow basic healthy lifestyle goals established by the American Heart Association, said Dr. Dana King, professor and chairman of the department of family medicine at West Virginia University, referencing his university's 2017 study comparing the healthy lifestyle rates of retired late-middle-aged adults with rates among those still working.
Kaiser Health News interviewed three other prominent experts on aging and health about how seniors can find the will to adopt healthier habits.
"People do financial planning for retirement, but what about retirement health planning?" King said.
Motivated seniors can begin by following KHN's 10-step program:
1. Buy great sneakers. Purchase a pair of top-quality sneakers specifically designed for walking, said Carolyn Rosenblatt, founder of AgingParents.com, who started participating in triathlons at age 63 and continues to do them at age 70. Start by walking around the block. Expand that to 30-minute walks at least three times weekly -- or set a goal to increase your walking distance 10 percent each week. And leave your sneakers by the front door.
2. Practice your balance. The best way to avoid falls is to retain a good sense of balance, said Rosenblatt. Practice standing on one leg with your eyes closed for at least 30 seconds.
3. Improve your breakfast. Stop eating the sweet roll with coffee. Consider substituting a home-blended smoothie with a banana, seasonal fruits, almond milk and protein powder or a protein patty without sugar. And cut out excess sugar in all your meals, said Rosenblatt. Replace soda with seltzer water.
4. De-stress wisely. Find ways to manage your stress that don't involve food, alcohol or smoking. There are lots of meditation programs you can download on your phone and listen to for even 10 minutes, said Rosenblatt.
5. Practice resistance training. To keep your muscle mass from disappearing, do resistance training by lifting dumbbells or barbells or using weight machines, said Kay Van Norman, owner of Brilliant Aging, a consulting firm for healthier aging. "Your muscles are amazing, but if you don't use them, you lose them," she said.
"""

aneg = """
Irma's path of destruction
Hurricane Irma is the strongest Atlantic basin hurricane ever recorded outside the Gulf of Mexico and the Caribbean Sea. It lasted as a hurricane from August 31 until September 11. The storm, which stretched 650 miles from east to west, affected at least nine US states, turning streets into rivers, ripping down power lines, uprooting trees and cutting off coastal communities.
On September 6, Hurricane Irma left a string of small Caribbean islands devastated. The eye of the hurricane passed over Barbuda, damaging about 95% of the buildings on the island.
The hurricane hit southwest Florida on September 10, battering the state's lower half and leaving a trail of tornadoes and storm-surge flooding as its core slowly moved inland.
The massive storm triggered evacuation orders for 5.6 million people before it made two landfalls.
On Monday, Irma was downgraded to a tropical storm as it lumbered through Georgia to parts north.
By Tuesday, Irma had left a trail of deadly devastation throughout the Southeast, flooding major cities including Jacksonville, Florida, and Charleston, South Carolina, and leaving millions without power.
"""

#Inserimento del testo
text = TextBlob(a)
text_1 = TextBlob(a, analyzer=NaiveBayesAnalyzer())
text2 = TextBlob(a2)
text2_1 = TextBlob(a2, analyzer=NaiveBayesAnalyzer())

text3 = TextBlob(a3)
text3_1 = TextBlob(a3, analyzer=NaiveBayesAnalyzer())
text4 = TextBlob(a4)
text4_1 = TextBlob(a4, analyzer=NaiveBayesAnalyzer())
text5 = TextBlob(a5)
text5_1 = TextBlob(a5, analyzer=NaiveBayesAnalyzer())

text_neg = TextBlob(aneg)
text_neg_1 = TextBlob(aneg, analyzer=NaiveBayesAnalyzer())

print("Sentiment1: ", text.sentiment)
print("Sentiment1_1: ", text_1.sentiment)
print("Sentiment2: ", text2.sentiment)
print("Sentiment2_1: ", text2_1.sentiment)
print("--------------------------------------")
print("Sentiment3: ", text3.sentiment)
print("Sentiment3_1: ", text3_1.sentiment)
print("Sentiment4: ", text4.sentiment)
print("Sentiment4_1: ", text4_1.sentiment)
print("Sentiment5: ", text5.sentiment)
print("Sentiment5_1: ", text5_1.sentiment)
print("--------------------------------------")
print("Sentiment_neg: ", text_neg.sentiment)
print("Sentiment_neg_1: ", text_neg_1.sentiment)