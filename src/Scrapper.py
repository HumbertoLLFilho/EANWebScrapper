from selenium import webdriver
from selenium.webdriver.common.by import By

import csv
import json

from bs4 import BeautifulSoup

with open("appsettings.json","r") as file:
    jsonData = json.load(file)

rootPath = jsonData["Paths"]["root"]

eans = []
descriptions=[]
eanFilePath = rootPath + "\\ListaDeEANsTest.csv"

with open(eanFilePath, newline='', encoding='utf-8') as file:
    line = 0
    reader = csv.reader(file, delimiter=';')

    for row in reader:
        if(line > 0):
            eans.append(row[0])
        
        line += 1

# Set up the browser
options = webdriver.ChromeOptions()
#options.add_argument('headless')
driver = webdriver.Chrome(options=options)


for ean in eans:
    description = {}

    url = f"https://cosmos.bluesoft.com.br/produtos/{ean}"

    # Navigate to the website
    driver.get(url)

    if(driver.find_elements(By.XPATH,"//button[@onclick='accept_lgpd()']")):
        submit_button = driver.find_element(By.XPATH,"//button[@onclick='accept_lgpd()']")
        submit_button.click()

    soup = BeautifulSoup(driver.page_source, 'html.parser', from_encoding="utf-8")
    
    span = soup.find('h1', {"class" : "page-header"})
    descriptionText = ''
    if(span is not None):
        cleanText = span.text.replace(';',',').replace('\n','')

        descriptionText = cleanText[:cleanText.index("GTIN")]
    else:
        descriptionText = "Não encontrado"
    
    description["EAN"] = ean
    description["DESCRIPTION"] = descriptionText
    descriptions.append(description)
    print(f"Ean salvo: {ean}")

driver.close()

filename = '\\EAN_NAMES.csv'
with open(rootPath+filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, delimiter=";", fieldnames= ['EAN','DESCRIPTION'])
    writer.writeheader()

    for description in descriptions:
        writer.writerow(description)