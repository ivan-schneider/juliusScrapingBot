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

# url2 = 'https://www.google.com/'
url = 'https://www.brastemp.com.br/geladeira-brastemp-inverse-3-frost-free-419-litros-cor-inox-com-freeze-control-pro-bry59ck/p?idsku=326031070&utmi_cp=cpc&utmi_campaign=cpc&gclid=Cj0KCQjwuNemBhCBARIsADp74QQr8AOLV3d-fgZVfsxlwFL8Hg9j3vdwh3vXrKvwFec9yVzbZN73gG4aAnnYEALw_wcB'
headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
browser = webdriver.Chrome()

site = requests.get(url, headers= headers)
soup = BeautifulSoup(site.content, 'html.parser')
loja = 'Site Brastemp'

bot_token: Final = '6424891430:AAHTgF7FhVjLiJXoyhuCbyeBWr56eMjRcq8'
bot: Final = '@maodevaca_bot'
chat_id: Final = '1279716179'


def send_message(token, chat_id, message):
    data = {"chat_id": chat_id, "text": msg}
    url = "https://api.telegram.org/bot{}/sendMessage".format(bot_token)
    requests.post(url, data)

def send_message_ping(token, chat_id, message):
    data1 = {"chat_id": chat_id, "text": msg_ping}
    url = "https://api.telegram.org/bot{}/sendMessage".format(bot_token)
    requests.post(url, data1)
    
## Variáveis de controle de preco e contador de chamados ##
preco_inicial = '0'
initial_count = 0

## Abre o navegador e realiza o request do site Brastemp ##
while True:
    try:
        initial_count += 1
        browser.get(url)
        time.sleep(5)
        
        if initial_count % 60 == 0:
            msg_ping = 'Ping'
            send_message_ping(bot_token, chat_id, msg_ping)
        ## Armazena o codigo fonte da página ##
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        ## Dentro da fonte armazenada, acha o elemento preco ## 
        p_tags = soup.find("div", class_="sc-gsnTZi").find_all("p")
        ## Para cada parágrafo, armazena no array o texto ##
        p_texts = []
        for p in p_tags:
         p_texts.append(p.get_text(strip=False))
    
        all_p_text = '\n'.join(p_texts)

        preco_dividido = soup.find("p", class_="sc-hKMtZM hUIHbE").find(class_="brastemp-componentsv2-2-x-currencyContainer").get_text(strip=True)
        preco_formatado = re.sub(r'[R$,\. ]', '', preco_dividido)
        preco_final = int(preco_formatado)
        
        # if preco_final < 740000:
        #     print('Now warriors!')
        # else:
        #     print('Wait for it!')
        # print(preco_formatado)
        # print(preco_final)
        
        if all_p_text != preco_inicial:
            print(all_p_text)
            preco_inicial = all_p_text
            msg = f'''{loja}\n{all_p_text}'''
            send_message(bot_token, chat_id, msg)       
        time.sleep(55)
    except:
        continue