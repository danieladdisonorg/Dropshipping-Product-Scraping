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


random=random.uniform(0,2)
login_url="https://www.larsson.pl/"
main_shop_url="https://mike.larsson.pl/pl/"

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-language":"ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding":"gzip, deflate, br, zstd",
    "Connection":"keep-alive",
    "Upgrade-Insecure-Requests":"1",
    "Content-Type":"text/html",
}
payload={
    "username":"106863",
    "password":"XVS12003440xv$"
}

chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Запускаем браузер в полном экране
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Скрываем автоматизацию
chrome_options.add_argument("--headless")    # Запуск браузера в фоновом режиме
# Устанавливаем драйвер
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

username = "106863"
password = "XVS12003440xv$"

# Открываем страницу логина
driver.get(login_url)

# Ждем, чтобы страница загрузилась
time.sleep(2)

# Находим поля для ввода логина и пароля
username_field = driver.find_element(By.ID, "username")
password_field = driver.find_element(By.ID, "password")

# Вводим логин и пароль
username_field.send_keys(username)
password_field.send_keys(password)

# Находим и нажимаем кнопку логина
login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
login_button.click()

# Ждем, чтобы страница загрузилась
time.sleep(2)
driver.get(main_shop_url)
time.sleep(3)
try:
    accept_all_button = WebDriverWait(driver, 4).until(
        ec.element_to_be_clickable((By.ID, "dv-t3-consent-management-button-accept-all"))
    )
    accept_all_button.click()
    print("Akceptuj wszystkie cookies- success..")
except Exception as e:
    print("ERROR!", e)
time.sleep(5)
main_shop_url_html=driver.page_source
with open("html/main_shop_url_html.html","w",encoding="utf8")as file:
    file.write(main_shop_url_html)
with open("html/main_shop_url_html.html",encoding="utf8") as file:
    src=file.read()
soup=BeautifulSoup(src,features="lxml")

main_data = re.compile("cat-item")
find_main_info = soup.find_all("div", class_=main_data)

list_of_links=[]
list_of_categories=[]
final_list=[
        ["Nazwa produktu",
        "Cena hurtowa",
        "Dostępność",
        "Grupa produktu",
        "№ art.",
        "Mini IMG",
        "Link do produktu"
         ]
]

with open("csv/larson_pl.csv","w",newline='', encoding="utf8") as file:
    writer=csv.writer(file)

for item in find_main_info:
    category_in_item=item.text.split(". ")
    category=category_in_item[1].replace("\xa0","")
    link_in_item=item.find("a")
    link=link_in_item.get("href")
    if category=="NOWOŚCI":
        continue
    list_of_categories.append(category)
    list_of_links.append(link)

def find_all_pages(src):
    soup=BeautifulSoup(src,features="lxml")
    try:
        last_page_find=soup.find("div",class_="navi_seiten").text
        last_page_count=last_page_find.split()
        last_page=int(last_page_count[len(last_page_count)-2])
    except:
        last_page=1
        print("*****WARNING! FOUND ONLY 1 PAGE!!*****")
    return last_page

def lets_pars(src, final_list) :
    soup = BeautifulSoup(src, features="lxml")
    main_block = soup.find("div", class_="gallery")
    all_items = main_block.find_all("div", class_="gal_elem kombi")
    for item in all_items:
        avi = item.find("div", class_="avail_wrap").text
        res=re.findall(r'\d+',avi)
        item_avi=res[0] if res else "0"
        item_name = item.find("h3").find("a").text
        item_link = item.find("h3").find("a").get("href")
        item_price_l = item.find("td", class_="gal_price_color larsson_size").text
        item_price = item_price_l.replace("\xa0", " ")
        item_image = item.find("img").get("src")
        item_category = item.find_previous("div", class_="breadcrump-liste").text.strip()
        category = " > ".join(
            re.sub(r'^\s*»?\s*\d*\.\s*', '', line.strip()) for line in item_category.strip().splitlines() if line.strip()
        )
        number=item.find("div", class_="gal_artnr").text.split(": ")
        item_num=number[1].replace("\xa0"," ")

        final_list.append([item_name, item_price, item_avi,  category, item_num, "https:"+item_image, item_link])
    return final_list

for i in range(len(list_of_categories)):
    driver.get(list_of_links[i]+"?show=gal_kombi")
    
    time.sleep(random)
    
    with open (f"html/{list_of_categories[i]}.html","w", encoding="utf8") as file:
        file.write(driver.page_source)
    with open (f"html/{list_of_categories[i]}.html", encoding="utf8") as file:
        src=file.read()
        
    last_page=find_all_pages(src)
    
    time.sleep(random)

    for pars_page in range(last_page-1):
        time.sleep(random)
        driver.get(list_of_links[i] + f"?show=gal_kombi&sr={pars_page*30}")
        src=driver.page_source
        lets_pars(src, final_list)
        print(f"Parsing {list_of_categories[i]}... page {pars_page+1} of {last_page}")


with open("csv/larson_pl.csv","a",newline='', encoding="utf8") as file:
    writer=csv.writer(file)
    for i in range(len(final_list)):
        writer.writerow(final_list[i])



driver.close()