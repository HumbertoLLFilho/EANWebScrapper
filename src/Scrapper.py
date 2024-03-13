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


def find_all_banks(driver:ChromiumDriver):
    banks:list[Banco] = []

    banks.append(find_featured_banks(driver))
    banks.append(find_other_banks(driver))

    return banks

#tile Promociones bancarias
def find_other_banks(driver: ChromiumDriver):
    banks: list[Banco] = []

    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[title="Promociones bancarias"]'))).click()

    payment_div = driver.find_elements(By.CLASS_NAME, "pm-list")

    if(payment_div):
        payment_li = payment_div[0].find_elements(By.TAG_NAME, "li")

        for payment in payment_li:
            payment.click()

            banks_li = driver.find_element(By.ID, "banks").find_elements(By.TAG_NAME,"option")

            for bank in banks_li:
                name = bank.text

                



    return banks




def find_featured_banks(driver):
    banks: list[Banco] = []

    banks_div = driver.find_elements(By.ID, "featured-offers-container")

    if(banks_div.__len__() != 0):
        banks_li = banks_div[0].find_elements(By.TAG_NAME, "li")
        
        for bank_info in banks_li:
            promotion = bank_info.find_element(By.CLASS_NAME, "promo-note").text
            name = bank_info.find_element(By.CSS_SELECTOR, "img").get_attribute("alt")
            price = bank_info.find_element(By.CLASS_NAME, "promo-amount").text
            
            banks.append(Banco(name, promotion, price))

    return banks

def find_price(soup: BeautifulSoup):
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

        price, past_price = find_price(soup)
        top_banks = find_featured_banks(driver)

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