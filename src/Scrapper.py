import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from Models.Banco import Banco
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import FileHelper


def find_banks(driver: ChromiumDriver):
    banks_div = driver.find_elements(By.ID, "featured-offers-container")






def find_banks(soup: BeautifulSoup):    
    bancos: list[Banco] = []

    banks_div = soup.find("div", {"id", "featured-offers-container"})

    banks_li = banks_div.select("[data-promotion-id]")

    if(banks_li.__len__() == 0):
        no_banks_listed = True
        i = 0
        while(no_banks_listed):
            time.sleep(0.5)
            banks_div = soup.find("div", {"id", "featured-offers-container"})
            banks_li = banks_div.select("[data-promotion-id]")
            
            if(banks_li.__len__() != 0 or i > 100):
                no_banks_listed = False

            i = i+1

    for bank_info in banks_li:
        promotion = bank_info.find_next("span", {"class", "promo-note"})
        name = bank_info.find_next("img")
        price = bank_info.find_next("span", {"class", "promo-amount"})

        bancos.append(Banco(name.attrs.get("alt"), promotion.text, price.text))

    return bancos

def findPrice(soup: BeautifulSoup):
    priceText = ''

    classs = {"": ""}

    prices_div = soup.find("div", {"class" : "promotion-default"})

    price = ''
    past_price = ''
    if(prices_div is not None):
        price_span = prices_div.find_next("span", {"class" : "price"})

        if(price_span is not None):
            price = price_span.text
            
        past_price_span = prices_div.find_next("span", {"data-price-type" : "oldPrice"})
        if(past_price_span is not None):
            past_price = past_price_span.text

    return price, past_price

rootPath = FileHelper.getPathFromAppsettings()
descriptions=[]
eanFilePath = rootPath + "\\Detalhes_produtos.csv"

details = FileHelper.OpenAndReadEansFile(eanFilePath)

# Set up the browser
options = webdriver.ChromeOptions()
#options.add_argument('headless')
driver = webdriver.Chrome(options=options)

for detail in details:
    description:dict[str,str] = {}

    # Navigate to the website
    if(detail.link != ''):
        driver.get(detail.link)

        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser', from_encoding="utf-8")
        
        wait = WebDriverWait(driver, 10)
        
        if(driver.find_elements(By.ID, "btnNoIdWpnPush")):
            wait.until(EC.element_to_be_clickable((By.ID, 'btnNoIdWpnPush'))).click()

        price, past_price = findPrice(soup)
        top_banks = find_banks(soup)

        description["Codigo"] = detail.codigo
        description["EAN"] = detail.ean
        description["Detalhe"] = detail.detalhe
        description["Marca"] = detail.marca
        description["Link consultado"] = detail.link
        description["Preço"] = price
        description["Preço antigo"] = past_price

        description["banco 1 nome"] = top_banks[0].name
        description["banco 1 parcelas"] = top_banks[0].installment
        description["banco 1 preço"] = top_banks[0].price

        description["banco 2 nome"] = top_banks[1].name
        description["banco 2 parcelas"] = top_banks[1].installment
        description["banco 2 preço"] = top_banks[1].price

        description["banco 3 nome"] = top_banks[2].name
        description["banco 3 parcelas"] = top_banks[2].installment
        description["banco 3 preço"] = top_banks[2].price

        descriptions.append(description)
        print(f"Ean salvo: {detail.ean}")

driver.close()

filename = '\\EansComDescricao.csv'
with open(rootPath+filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, delimiter=";", fieldnames= description.keys())
    writer.writeheader()

    for description in descriptions:
        writer.writerow(description)