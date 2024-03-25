from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from Models.Installment import Installment
from Models.Product import Product
from FileHelper import FileHelper
from selenium import webdriver
from bs4 import BeautifulSoup
from Models.Bank import Bank
from Models.Card import Card
import pandas as pd
import time

file_helper = FileHelper()

rootPath = file_helper.getPathFromAppsettings()
eanFilePath = rootPath + "\\Detalhes_produtos.csv"

products:list[Product]=[]
installments:list[Installment]=[]
banks_db:list[Bank]= []
cards_db:list[Card]= []

def find_all_installments(driver: ChromiumDriver, product: Product):
    installments: list[Installment] = []

    wait = WebDriverWait(driver, 10)

    a_banks_promotions = driver.find_element(By.CSS_SELECTOR, 'a[title="Promociones bancarias"]')
    h4_banks_promotions = a_banks_promotions.find_element(By.TAG_NAME,"h4")

    wait.until(EC.element_to_be_clickable(h4_banks_promotions)).click()

    cards_modal = driver.find_element(By.ID, "modal-installments-calculator")
    card_div = cards_modal.find_elements(By.CLASS_NAME, "payment-methods")

    if(card_div):
        card_li = card_div[0].find_elements(By.TAG_NAME, "li")

        for card_element in card_li:
            wait.until(EC.element_to_be_clickable(card_element)).click()

            card_name = card_element.find_element(By.TAG_NAME, "img").get_attribute("alt")

            banks_div = driver.find_element(By.ID, "banks")
            banks_select = Select(banks_div)
            banks_options = banks_div.find_elements(By.TAG_NAME,"option")

            for bank_web_element in banks_options:
                bank_name = bank_web_element.text
                banks_select.select_by_visible_text(bank_name)

                bank = next((x for x in banks_db if x.name == bank_name), None)
                if(bank == None):
                    bank = Bank(bank_name)

                    banks_db.append(bank)
                
                card = next((x for x in cards_db if x.name == card_name and x.bank_id == bank.id), None)
                if(card == None):
                    card = Card(bank.id, card_name, bank)

                    cards_db.append(card)

                installments_div = cards_modal.find_elements(By.CLASS_NAME, "installment")

                for installment_element in installments_div:
                    strong = installment_element.find_element(By.TAG_NAME, "strong").text

                    installment_quantity = strong.split(' ')[0]
                    installment_price = strong.partition("$")[2].split(' ')[0].replace(".","")
                    
                    refound_porcentage = strong.partition("+ ")[2].partition("%")[0]
                    if(refound_porcentage == ""):
                        refound_porcentage = 0
                    
                    is_interest_free = "sin interés" in strong

                    installment = Installment(product.id, card.id, installment_quantity, installment_price, refound_porcentage, is_interest_free, card, product)

                    installments.append(installment)

    return installments

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

    return price.replace("$", "").replace(".",""), past_price.replace("$", "").replace(".","")

details = file_helper.OpenAndReadEansFile(eanFilePath)

# Set up the browser
options = webdriver.ChromeOptions()
#options.add_argument('headless')
driver = webdriver.Chrome(options=options)

for detail in details:
    product: Product = None
    extracted_installments = []

    price = 0
    past_price = 0

    if(detail.link != ''):
        driver.get(detail.link)

        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser', from_encoding="utf-8")
        
        wait = WebDriverWait(driver, 10)
        
        if(driver.find_elements(By.ID, "btnNoIdWpnPush")):
            wait.until(EC.element_to_be_clickable((By.ID, 'btnNoIdWpnPush'))).click()

        price, past_price = find_price(soup)

        product = Product(detail.codigo, detail.ean, detail.detalhe, detail.marca, detail.link, past_price, price)
        extracted_installments = find_all_installments(driver, product)
    
    if(product == None):
        product = Product(detail.codigo, detail.ean, detail.detalhe, detail.marca, detail.link, past_price, price)

    products.append(product)
    installments.extend(extracted_installments)
    
    print(f"Ean salvo: {detail.ean}")

driver.close()

products_dict: list[dict[str,str]] = [{}]
for product in products:
    products_dict.append(product.to_dict())

installments_dict: list[dict[str,str]] = [{}]
for installment in installments:
    installments_dict.append(installment.to_dict())
    
banks_dict: list[dict[str,str]] = [{}]
for bank in banks_db:
    banks_dict.append(bank.to_dict())
    
cards_dict: list[dict[str,str]] = [{}]
for card in cards_db:
    cards_dict.append(card.to_dict())

products_df = pd.DataFrame(products_dict)
installments_df = pd.DataFrame(installments_dict)
banks_df = pd.DataFrame(banks_dict)
cards_df = pd.DataFrame(cards_dict)

file_helper.write_sheet(products_df, "Produtos")
file_helper.append_sheet(installments_df, "parcelas")
file_helper.append_sheet(banks_df, "bancos")
file_helper.append_sheet(cards_df, "cartões")