import requests
from bs4 import BeautifulSoup
import lxml.etree as et
import pandas as pd 
import time
import random

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36"
}

# Function to get the DOM with retries
def get_dom(the_url, retry_delay=7):
    try:
        response = requests.get(the_url, headers=header)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        soup = BeautifulSoup(response.text, 'html.parser')
        dom = et.HTML(str(soup))
        return dom
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        time.sleep(retry_delay)
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(retry_delay)

base_url_zero = "https://www.vivareal.com.br"
base_url= "https://www.vivareal.com.br/aluguel/santa-catarina/florianopolis/?pagina=" 

pages_url = []    
listing_url = []

for i in range(1, 3): 
    page_url = base_url + str(i)
    pages_url.append(page_url) 
    
a_elements_xpath = '//*[contains(concat(" ", normalize-space(@class), " "), " property-card__main-info ")]//a[@href]'

for page in pages_url:
    dom = get_dom(page)
    if dom is not None:
        hrefs = dom.xpath(a_elements_xpath)

        for href in hrefs:
            listing_url.append(base_url_zero + href.get('href'))

        time.sleep(random.randint(1, 3))

def get_price(dom):
    price = dom.xpath('//*[@id="js-site-main"]/div[2]/div[2]/div[1]/div/div[1]/div/h3/text()')[0]
    return price

def get_n_room(dom):
    n_room = dom.xpath('//*[@id="js-site-main"]/div[2]/div[1]/div[4]/ul/li[2]/text()')[0]
    return n_room

def get_area(dom):
    area = dom.xpath('//*[@id="js-site-main"]/div[2]/div[1]/div[4]/ul/li[1]/text()')[0]
    return area

values_dict = {
    'link': [], 'price': [], 'area': [],
    'n_room': [], 
    
}

for page in listing_url:
    dom = get_dom(page)
    if dom is not None:
        
        price = get_price(dom)
        area = get_area(dom)
        n_room = get_n_room(dom)

        values_dict['link'].append(page)
        values_dict['price'].append(price)
        values_dict['area'].append(area)
        values_dict['n_room'].append(n_room)

        time.sleep(random.randint(1, 4))

df = pd.DataFrame(values_dict)

print(df)