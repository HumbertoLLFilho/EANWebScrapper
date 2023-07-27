import requests
import csv

from bs4 import BeautifulSoup

rootPath = "C:\\Users\\Humberto\\Desktop\\Dev\\EAN web scrapper\\"

eans = [
    "7896964625853",
    "7896460317801",
    "7908414431768",
    "7908414422964",
    "7908414422926",
    "673419339759",
    "673419318730"
]

descriptions=[]

for ean in eans:
    description = {}

    URL = f"https://www.google.com/search?q={ean}"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html.parser', from_encoding="utf-8") # If this line causes an error, run 'pip install html5lib' or install html5lib
    
    img = soup.find('img')
    if(img is not None):
        alt = img['alt']
        
        description["EAN"] = ean
        description["DESCRIPTION"] = alt.replace(';',',')

        descriptions.append(description)
    
    print(f"Ean salvo: {ean}")

filename = 'EAN_NAMES.csv'
with open(rootPath+filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, delimiter=";", fieldnames= ['EAN','DESCRIPTION'])
    writer.writeheader()

    for description in descriptions:
        writer.writerow(description)