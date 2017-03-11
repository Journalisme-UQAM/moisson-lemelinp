#coding: utf-8

import csv
import requests
from bs4 import BeautifulSoup
import re
#La fonction re (Regular Expressions) permet de trouver des url qui changent de fin. Très utile pour le scraping!

url = "http://www.geonet.org.nz/quakes/felt"
#J'ai choisi cette section du site pour exclure les tremblements de terre minimes («unnoticeable») qui sont nombreux et moins pertinents.

r = requests.get(url)

soup = BeautifulSoup(r.content,"html.parser")

n = 0

# for link in soup.findAll('a', href=re.compile('/quakes/region/newzealand/.+')):
    # if link.text:
        # a = link["href"]
        # url = "http://www.geonet.org.nz%s" % a
        # print(url)
        #Avec ça, je peux afficher tous les url "quake details" pour chacune des trente entrées

for link in soup.findAll('a', href=re.compile('/quakes/region/newzealand/.+')):
    if link.text:
        a = link["href"]
        n += 1
        url2 = "http://www.geonet.org.nz%s" % a
        b = requests.get(url2)
        soup2 = BeautifulSoup(b.content, "html.parser")
        table = soup2.find("table",{"class":"table table-hover table-condensed"})
        rows = list()
        for row in table.findAll("tr"):
            rows.append(row.text)
        print(n,rows)
        
#Le script nous donne toutes les informations qui sont dans le tableau «Quake Details» pour chacun des tremblements de terre (30 plus récents)
