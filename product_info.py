from enum import member
from random import Random

from bs4 import BeautifulSoup
import lxml
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from urllib3.filepost import writer
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import re
import csv

url="xxxxx"
clean_xxx_pl=[
    ["Nazwa produktu", "Cena hurtowa", "№ art", "Dostępność", "Image", "Pasuje do pojazdów" ," Grupa produktu"]
]
with open("csv/clean_xxx.csv","w", newline="", encoding="utf-8") as file:
    writer=csv.writer(file)

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-language":"ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding":"gzip, deflate, br, zstd",
    "Connection":"keep-alive",
    "Upgrade-Insecure-Requests":"1",
    "Content-Type":"text/html",
}
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Запускаем браузер в полном экране
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Скрываем автоматизацию
chrome_options.add_argument("--headless")    # Запуск браузера в фоновом режиме

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
options = webdriver.ChromeOptions()


driver.get(url)
time.sleep(3)
try:
    accept_all_button = WebDriverWait(driver, 4).until(
        ec.element_to_be_clickable((By.ID, "dv-t3-consent-management-button-accept-all"))
    )
    accept_all_button.click()
    print("Akceptuj wszystkie cookies- success..")
except Exception as e:
    print("ERROR!", e)
time.sleep(3)

url_wo_login=driver.page_source

with open("html/url_wo_login.html","w", encoding="utf8") as file:
    file.write(url_wo_login)

try:
    wait = WebDriverWait(driver, 4)
    button = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "anonum_btn")))
    button.click()
    print("Wejdź bez logowania - success..")
except Exception as e:
    print("ERROR", e)

with open("csv/xxx_pl.csv", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)
    data = list(reader)
for row in data:
    url=row[6]
    driver.get(url)
    item_html=driver.page_source
    with open("html/item_html.html", "w", encoding="utf8") as file:
        file.write(item_html)
    with open("html/item_html.html", encoding="utf8") as file:
        src = file.read()
    soup = BeautifulSoup(src, features="lxml")
    try:
        current_img = soup.find("a", class_="detail_img current_image").get("href")
        img = f"https:{current_img}"
    except:
        img = "No Image"

    try:
        all_models = soup.find_all("tr", class_="tda")
        models = []
        models_list=[]
        for item in all_models:
            model_info = item.find_all("a")
            items_list = []
            for items in model_info:
                items_list.append(items.text)
            model = items_list[0]
            year = items_list[5]
            if model.strip() in models_list:
                models_list.append(year.strip())
            else:
                models_list.append(model.strip())
                models_list.append(year.strip())
        models = " ".join(models_list)
    except:
        models = "No models info"
    clean_xxx_pl.append([row[0],row[1],row[4],row[2],img,models, row[3]])
    i+=1
    print(f"Done {i} of {len(data)}")
with open("csv/clean_xxx_pl.csv","w", newline="", encoding="utf-8") as file:
    writer=csv.writer(file)
    for j in range(len(clean_xxx_pl)):
        writer.writerow(clean_xxx_pl[j])
driver.quit()
