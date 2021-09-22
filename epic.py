import requests
from bs4 import BeautifulSoup
import csv
import time
import concurrent.futures

CSV = 'DATAEST.csv'
HOST = 'https://epicentrk.ua'
URL = 'https://epicentrk.ua/ua/brands/estares.html'
PAGE = '?PAGEN_1='
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}
def pars_URL(url):
    soup = BeautifulSoup(get_html(url).text, 'html.parser')
    list_groups1 = soup.find_all('a', class_="shop-category__list-title link link--inverted nc", href=True)
    list_groups = [a['href'] for a in list_groups1]
    return list_groups

def get_html(url):#fucn
    response = requests.get(url, headers=HEADERS)
    return response

def last_page(url):    
    soup = BeautifulSoup(get_html(url).text, 'html.parser')
    last_page_num = soup.find_all('a', class_="custom-pagination__item ng-star-inserted")
    try:
        number = int([i.text for i in last_page_num][-1])
    except Exception as e:
        print(e)
        number = 1
    return number

def get_page(number, url):
    page_list = []
    for page in range(1,number+1):
        page_list.append(url+PAGE+str(page))
    return page_list

def get_list_links(page_num, url):#list
    products_links = []
    list_response = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url_page in get_page(page_num, url):
            futures.append(executor.submit(get_html, url=url_page))
        for future in concurrent.futures.as_completed(futures):
            list_response.append(future.result())
    for resp in list_response:
        soup = BeautifulSoup(resp.text, 'html.parser') # Parse the HTML as a string    
        for a in soup.find_all("a", class_="card__photo", href=True):
            products_links.append(a['href'])
    return products_links

def get_response(page_num, url):
    list_response = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url in get_list_links(page_num, url):
            futures.append(executor.submit(get_html, url=HOST+url))
        for future in concurrent.futures.as_completed(futures):
            list_response.append(future.result())
    return list_response
  
def get_contents(response):
    soup2 = BeautifulSoup(response.text, 'html.parser')  
    products_dict = {}
    try:
        title = soup2.find_all('h1', class_="p-header__title nc")[0].text
    except Exception as e:
        try:
            
            title = soup2.find_all('div', class_="row head-panel product-head align-justify")[0].text
        except:
            return {'timeout': None}

    products_dict['title'] = str(title)
    try:
        img_link = soup2.find_all('img', class_="p-slider__photo")[0]['src']
    except IndexError:
        try:
            img_link = soup2.find_all('img', class_="swiper-lazy")[0]['src']
        except IndexError:
            img_link = soup2.find_all('img', class_="product-single-image")[0]['src']
    
    products_dict['img_link'] = str(img_link)
    
    def get_art():
        art_block = soup2.find_all('div', class_="p-block__row p-block__row--status")[0]
        str_for_pars = str(art_block.find_all('div')[1])
        index_str = str_for_pars.index('"articul": "')
        index_art = index_str+len('"articul": "')
        articul = str_for_pars[index_art:index_art+8]
        return articul
    def get_art2():
        art_block = soup2.find_all('div', class_="info-row align-justify")[0]
        articul = str(art_block.find_all('span', class_="sticker code")[0].text)
        return articul    
    try:
        products_dict['articul'] = get_art()
    except:
        products_dict['articul'] = get_art2()
    
    def get_char():
        char = soup2.find('div', class_='p-block__row p-block__row--char-all').find_all('ul', class_='p-char')
        char_name_list = []
        char_value_list = []
        for char_c in char:
            for li in char_c.find_all('li', class_='p-char__item'):
                for span in li.find_all('span', class_='p-char__name-value'):
                    char_name_list.append(span.text.strip(':\u2002'))
                for span in li.find_all('span', class_='p-char__value'):
                    w = span.text
                    w = w.replace(u'\xa0', u' ').replace(u'\u20b4', u'грн')
                    char_value_list.append(w)
        char_dict = dict(zip(char_name_list,char_value_list))
        return char_dict
    def get_char2():
        char = soup2.find('section', class_='product__characteristics').find_all('ul', class_='option__list option__list--hide-content option__list--show-all')
        char_name_list = []
        char_value_list = []
        for char_c in char:
            for li in char_c.find_all('li', class_='option__item'):
                for span in li.find_all('span', class_='option__name--text'):
                    char_name_list.append(span.text.strip(':\u2002'))
                for span in li.find_all('span', class_='option__value'):
                    w = span.text
                    w = w.replace(u'\xa0', u' ').replace(u'\u20b4', u'грн')
                    char_value_list.append(w)
        char_dict = dict(zip(char_name_list,char_value_list))
        return char_dict
                    
    try:
        products_dict['char'] = get_char()  
    except:
        products_dict['char'] = get_char2()   
      
    return products_dict

def csv_record(items, path):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Name','Photo','ART','Characteristics'])
        for item in items:
            try:
                writer.writerow([item['title'],item['img_link'],item['articul'],item['char']])
            except:
                print('no data')
                continue
def start():
    products_list = []
    groups = pars_URL(URL)
    i = 1
    for group in groups:  
        page_num = last_page(HOST+group)
        #print(f"Количество продуктов: {len(get_list_links(page_num, HOST+group))}")
        print(i)
        i += 1
        for response in get_response(page_num, HOST+group):
            products_list.append(get_contents(response))
    csv_record(products_list, CSV)
    print('DONE')
if __name__ == '__main__':
    start_time = time.time()
    start()
    print("--- %s seconds ---" % (time.time() - start_time))