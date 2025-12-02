from bs4 import BeautifulSoup
import math

savegame = "C:\\Users\\[nutzername]\\AppData\\Roaming\\StardewValley\\Saves\\[spielername]_XXXXXXXXX\\[spielername]_XXXXXXXXX"

def setData(res):
	#einzelne items suchen und ausrechnen wie viel wert die sind
	for j in res:
		#quali: qualität des items
		quali = int(j.find("quality").text)
		#price: grundwert des items und wird mit der qualität verrechnet
		price = int(j.find("price").text)
		price = int((price * (1.0 + 0.25 * quali)))
		#stack: anzahl des items
		stack = int(j.find("stack").text)
		name = j.find("name").text
		
		#item mit speziellen faktor zur rechnung
		if name == "Salmonberry":
			price = int(price * 3.3)
		if name == "Blackberry":
			price = int(price * 3.3)
		
		#hinzurechnen des faktors für berufungen
		for i in multi_11:
			if name == i:
				price = int(price * 1.1)
		
		for i in multi_14:
			if name == i:
				price = int(price * 1.4)
		
		for i in multi_15:
			if name == i:
				price = int(price * 1.5)
		
		for i in multi_208:
			if name == i:
				price = int(price * 2.08)
			
		#hinzufügen der qualitätsstufe in den namen
		name = name + " " + str(quali)
		
		'''
		value = value + stack * price
		items = items + stack
		'''
		
		#hinzufügen des items in ein dict
		if name in data:
			data[name][1] += stack
		else:
			data[name] = [0, stack, price]



value = 0
items = 0
data = {}

#manche items werden mit einem multiplikator berechnet, was je nach berufung des character variiert.
#multi_11 = faktor 1,1
#multi_14 = faktor 1,4 usw
multi_11 = []
multi_14 = ["Blackberry Jelly", "Dried Blackberry", "Butter", "Strawberry Wine", "Strawberry Jelly", "Cheese", "Cloth", "Goat Cheese"]
multi_15 = []
multi_208 = []

#öffnen des savegames und ersetzen von sonderzeichen
#encoding schien nicht zu funktionieren
fp = open(savegame, "r")
c = fp.read()
c = c.replace("\u2013", "ö")
c = c.replace("\u0178", "ss")

#parsen mit bs4 und suchen von allen truhen auf dem hof.
#savegame ist im xml format
soup = BeautifulSoup(c, "lxml")
result = soup.find_all("object", {"xsi:type": "Chest"})#, {"xsi:type": "Chest"}

#es wird speziel nach großen truhen gesucht mit einer bestimmten farbe
for i in result:
	if i.itemid.text == "BigChest":
		if i.playerchoicecolor.r.text == "85" and i.playerchoicecolor.g.text == "85" and i.playerchoicecolor.b.text == "255":
			for j in i:
				res = j.find_all("item", {"xsi:type": "Object"})
				setData(res)

				res = j.find_all("item", {"xsi:type": "ColoredObject"})
				setData(res)
				
				res = j.find_all("item", {"xsi:type": "Torch"})
				setData(res)

#ausrechnen einzelner gesamtwerte von items und wert aller items
for i in data:
	data[i][0] = data[i][1]*data[i][2]
	value = value + data[i][1]*data[i][2]
	print (data[i])

#parsen von der angabe wie viele tage man schon gespielt hat
for i in soup.savegame.player.stats.values:
	if "daysPlayed" in i.text:
		days = int(str(i.text).replace("daysPlayed", ""))

#ausrechnen wann man 999.999 credits hat
final = math.ceil(days/(value/9999.99)*100)
jahr = math.floor(final/112)
jahreszeit = math.ceil(4*((final/112)-jahr))
tag = final-(jahr*112)-((jahreszeit-1)*28)

#ausgabe
print ("Fortschritt in Prozent:", round(value/9999.99,2), "%")
print ("Enddatum:")
print ("Jahr:", jahr)
print ("Jahreszeit:", jahreszeit)
print ("Tag:", tag)
