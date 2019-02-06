'''
7 donut plot (uno per paese)
Onuno con le percenutali della categoria sul paese
Esempio: Italia: 27% politica; 30% sport; ecc.. (numeri casuali)

QUERY:
SELECT categoria, COUNT(*)
FROM articoli JOIN (SELECT dlink, paese
					FROM notizie JOIN sitiweb
					WHERE paese = "")
GROUP BY categoria
'''