import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import Final
from telegram import Bot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import asyncio
import nest_asyncio
from bs4 import BeautifulSoup
import re

amazon = 'https://www.amazon.com.br/Geladeira-Frost-Free-Panasonic-Escovado/dp/B08KH1VYGF/ref=sr_1_5?brr=1&qid=1695350664&rd=1&refinements=p_89%3APanasonic%2Cp_n_feature_ten_browse-bin%3A118645779011&rnid=75337509011&s=appliances&sr=1-5&ufe=app_do%3Aamzn1.fos.25548f35-0de7-44b3-b28e-0f56f3f96147&th=1'
panasonic = 'https://loja.panasonic.com.br/geladeira-frost-free-panasonic-aco-escovado-nr-bb71pvfx/p?skuId=45012'
carrefour = 'https://www.carrefour.com.br/geladeira-panasonic-a-frost-free-480l-aco-escovado-nr-bb71pvfx-220v-5942870/p'
headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
browser = webdriver.Chrome()
# wait = WebDriverWait(browser, 5)

# site = requests.get(panasonic, headers= headers)
# soup = BeautifulSoup(site.content, 'html.parser')

bot_token: Final = '6424891430:AAHTgF7FhVjLiJXoyhuCbyeBWr56eMjRcq8'
bot: Final = '@maodevaca_bot'
chat_id: Final = '1279716179'


def send_message(token, chat_id, message):
    data = {"chat_id": chat_id, "text": msg}
    url = "https://api.telegram.org/bot{}/sendMessage".format(bot_token)
    requests.post(url, data)
    
## Variáveis de controle de preco e contador de chamados ##
initial_count = 0
p_preco_avista_inicial = '0'
p_preco_parcelado_inicial = '0'
a_preco_avista_inicial = '0'
a_preco_parcelado_inicial = '0'
c_preco_avista_inicial = '0'
c_preco_parcelado_inicial = '0'

## Abre o navegador e realiza o request do site desejado##
while True:
    try:
        ## Contador de chamados aos sites para ping 
        initial_count += 1
        if initial_count % 120 == 0:
            msg = 'Ping'
            send_message(bot_token, chat_id, msg)

        browser.get(panasonic)
        time.sleep(10)
        ## Armazena o codigo fonte da página ##
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
     
        p_preco_avista =  soup.find("span", class_="vtex-product-price-1-x-sellingPriceValue vtex-product-price-1-x-sellingPriceValue--compra-flutuante").get_text(strip=False)
        p_preco_parcelado = soup.find("span", class_="vtex-product-price-1-x-installments vtex-product-price-1-x-installments--compra-flutuante").get_text(strip=False)

        # print('Panasonic ' + p_preco_avista)
        # print('Panasonic ' +  p_preco_parcelado)

        browser.get(amazon)
        time.sleep(10)
        ## Armazena o codigo fonte da página ##
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
     
        a_preco_avista =  soup.find("span", class_="a-offscreen").get_text(strip=False)
        a_preco_parcelado = soup.find("span", class_="best-offer-name a-text-bold").get_text(strip=False)

        # print('Amazon ' + a_preco_avista)
        # print('Amazon ' +  a_preco_parcelado)

        browser.get(carrefour)
        time.sleep(10)
        ## Armazena o codigo fonte da página ##
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
     
        c_preco_avista =  soup.find("span", class_="carrefourbr-carrefour-components-0-x-currencySellingPrice").get_text(strip=False)
        c_preco_parcelado = soup.find("div", class_="carrefourbr-carrefour-components-0-x-installmentPrice").get_text(strip=False)

        # print('Carrefour ' + c_preco_avista)
        # print('Carrefour ' +  c_preco_parcelado)

        if  p_preco_avista_inicial != p_preco_avista or p_preco_parcelado_inicial != p_preco_parcelado or a_preco_avista_inicial != a_preco_avista or a_preco_parcelado_inicial != a_preco_parcelado or c_preco_avista_inicial != c_preco_avista or c_preco_parcelado_inicial != c_preco_parcelado:
            print('Panasonic ' + p_preco_avista)
            print('Panasonic ' +  p_preco_parcelado)
            print('Amazon ' + a_preco_avista)
            print('Amazon ' +  a_preco_parcelado)
            print('Carrefour ' + c_preco_avista)
            print('Carrefour ' +  c_preco_parcelado)
            p_preco_avista_inicial = p_preco_avista
            p_preco_parcelado_inicial = p_preco_parcelado
            a_preco_avista_inicial = a_preco_avista
            a_preco_parcelado_inicial = a_preco_parcelado
            c_preco_avista_inicial = c_preco_avista
            c_preco_parcelado_inicial = c_preco_parcelado
            msg = f'''{'Site Panasonic'}\n{p_preco_avista + '  a vista'}\n{p_preco_parcelado}\n\n{'Site Amazon'}\n{a_preco_avista + '  a vista'}\n{a_preco_parcelado}\n\n{'Site Carrefour'}\n{c_preco_avista + '  a vista'}\n{c_preco_parcelado}'''
            send_message(bot_token, chat_id, msg)       
        time.sleep(30)
    except:
        continue
