import pandas as pd
import requests
import re
import logging
from datetime import datetime
from bs4 import BeautifulSoup

logging.basicConfig(filename='app.log',filemode='a',format='%(asctime)s - %(message)s',level=logging.INFO,  datefmt='%Y-%m-%d %H:%M:%S')
models  = ['RTX 6800','RTX 3080','RTX 6700']
now = datetime.now()
now_formatted = now.strftime("%Y%m%d_%H%M%S")

def extract_source(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
    source=requests.get(url, headers=headers).text
    return source

def create_search_term(i):
    i = i.replace(' ','+')
    return i

try:
    for model in models:
        keyword = create_search_term(model)
        url = r'https://www.bestbuy.com/site/searchpage.jsp?id=pcat17071&qp=category_facet%3DGPUs%20%2F%20Video%20Graphics%20Cards~abcat0507002&st={}'.format(keyword)
        t = extract_source(url)
        soup = BeautifulSoup(t,'html.parser')
        model_span = soup.findAll('span',class_='sku-value')
        price_div = soup.findAll('div',class_='priceView-hero-price priceView-customer-price')
        available_div = soup.findAll('div' ,class_='fulfillment-add-to-cart-button')
        available = [x.text for x in available_div]
        model_name = []
        for i in model_span:
            if len(i.text) > 7:
                model_name.append(i.text)
        pattern = re.compile("[\\$][0-9.,]+")
        price  = []
        for i in price_div:
            price.append(pattern.match(i.text)[0])
        df = pd.DataFrame({"model_name":model_name,"Price":price,"Available":available})
        df.to_csv('results//'+model+'_'+now_formatted+'.csv')
except Exception as e:
    logging.error(e)

logging.info('App Completed ')

