### MES COMMENTAIRES ET CORRECTIONS SONT MARQUÉS PAR TROIS DIÈSES

#coding: utf-8

import csv
import requests
from bs4 import BeautifulSoup
import re
#La fonction re (Regular Expressions) permet de trouver des url qui changent de fin. Très utile pour le scraping!

url = "http://www.geonet.org.nz/quakes/felt"
#J'ai choisi cette section du site pour exclure les tremblements de terre minimes («unnoticeable») qui sont nombreux et moins pertinents.

### Il est toujours préférable de s'identifier quand on fait du scraping comme journaliste
### Même sur un site aux antipodes

r = requests.get(url) ### Ici, il aurait fallu ajouter une entête
soup = BeautifulSoup(r.content,"html.parser")

n = 0

# for link in soup.findAll('a', href=re.compile('/quakes/region/newzealand/.+')):
    # if link.text:
        # a = link["href"]
        # url = "http://www.geonet.org.nz%s" % a
        # print(url)
        #Avec ça, je peux afficher tous les url "quake details" pour chacune des trente entrées

for link in soup.findAll('a', href=re.compile('/quakes/region/newzealand/.+')): ### Je reconnais l'ancien version de BeautifulSoup ("findAll" au lieu de "find_all")
    if link.text:
        a = link["href"]
        n += 1
        url2 = "http://www.geonet.org.nz%s" % a
        b = requests.get(url2)
        soup2 = BeautifulSoup(b.content, "html.parser")
        table = soup2.find("table",{"class":"table table-hover table-condensed"})
        rows = list()
        for row in table.findAll("tr"):
            # rows.append(row.text) ### Cette commande prend tout le texte de chacune des lignes. Il y a deux <td>. On n'a besoin que du second.

### Il peut aussi être intéressant de transformer certaines infos en nombres, notamment les coordonnées afin de placer ce points sur une carte
            if row.find("td").text != "Type": ### Je saute les tremblements de terre qui incluent cette ligne, car lorsqu'elle est présente, sa valeur est toujours «earthquake»...
                if row.find("td").text == "Depth":
                    prof = float(row.find("td").find_next("td").text[:-3])
                    rows.append(prof)
                elif row.find("td").text == "Magnitude":
                    mag = float(row.find("td").find_next("td").text)
                    rows.append(mag)
                elif row.find("td").text == "Latitude, Longitude":
                    longLat = row.find("td").find_next("td").text.split(",")
                    latitude = longLat[0].strip()
                    longitude  = longLat[1].strip()
                    rows.append(latitude)
                    rows.append(longitude)
                else:
                    rows.append(row.find("td").find_next("td").text)
        print(n,rows)

### Il restait simplement à placer les infos recueillies par ton script dans un fichier CSV

        wellington = open("tremblements-de-terre-NZ-JHR.csv","a")
        auckland = csv.writer(wellington)
        auckland.writerow(rows)

# Le script nous donne toutes les informations qui sont dans le tableau «Quake Details» pour chacun des tremblements de terre (30 plus récents)
# Je ne te cacherai pas que j'ai eu de l'aide pour faire le travail. 
# J'ai parlé à un ami qui s'y connait beaucoup plus en informatique (et donc, qui sait quelles questions poser à Stack Overflow) 
# et je n'aurais jamais réussi le travail sans lui. 
# J'ai tout de même appris qu'il existe d'autres façons d'extraire des données d'une page.
# La fin du script avec la variable "row" est la principale différence
# BeautifulSoup comprend les tableaux et il peut extraire le texte dans chacune des rangées du tableau d'un seul coup!
# A mon avis, c'est beaucoup plus simple de procéder comme ça parce plutot que d'extraire un à la fois chacun des éléments qu'on cherche.
