import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import csv
import time


CSV = 'DATA.csv'
HOST = 'https://www.zooplus.de'
URL = 'https://www.zooplus.de/tierarzt/results'
params = {'animal_99': 'true', 'page': '1'}



session = HTMLSession()
r = session.get('https://www.zooplus.de/tierarzt/results?animal_99=true&page=1')
print(r.text)




def get_html(url: str, headers: dict, params: dict, cookies: dict) -> 'bs4.BeautifulSoup':
    response = requests.get(url, headers=headers, params=params, cookies=cookies)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

print(BeautifulSoup(requests.get(URL).text, 'lxml'))

#print(get_html(URL, HEADERS, params, cookies))#.find_all('a', class_="result-intro"))#[0].text)


def get_response(page_num, url):
    list_response = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url in get_list_links(page_num, url):
            futures.append(executor.submit(get_html, url=HOST+url))
        for future in concurrent.futures.as_completed(futures):
            list_response.append(future.result())
    return list_response


# def get_contents(soup: soup) -> dict:
#     contents_dict = {}
#     try:
#         title = soup.find_all('a', class_="result-intro")#[0].text
#     except Exception as e:
#         try:
#
#             title = soup2.find_all('div', class_="row head-panel product-head align-justify")[0].text
#         except:
#             return {'timeout': None}
#
#     products_dict['title'] = str(title)
#     try:
#         img_link = soup2.find_all('img', class_="p-slider__photo")[0]['src']
#     except IndexError:
#         try:
#             img_link = soup2.find_all('img', class_="swiper-lazy")[0]['src']
#         except IndexError:
#             img_link = soup2.find_all('img', class_="product-single-image")[0]['src']
#
#     products_dict['img_link'] = str(img_link)
#
#     def get_art():
#         art_block = soup2.find_all('div', class_="p-block__row p-block__row--status")[0]
#         str_for_pars = str(art_block.find_all('div')[1])
#         index_str = str_for_pars.index('"articul": "')
#         index_art = index_str+len('"articul": "')
#         articul = str_for_pars[index_art:index_art+8]
#         return articul
#     def get_art2():
#         art_block = soup2.find_all('div', class_="info-row align-justify")[0]
#         articul = str(art_block.find_all('span', class_="sticker code")[0].text)
#         return articul
#     try:
#         products_dict['articul'] = get_art()
#     except:
#         products_dict['articul'] = get_art2()
#
#     def get_char():
#         char = soup2.find('div', class_='p-block__row p-block__row--char-all').find_all('ul', class_='p-char')
#         char_name_list = []
#         char_value_list = []
#         for char_c in char:
#             for li in char_c.find_all('li', class_='p-char__item'):
#                 for span in li.find_all('span', class_='p-char__name-value'):
#                     char_name_list.append(span.text.strip(':\u2002'))
#                 for span in li.find_all('span', class_='p-char__value'):
#                     w = span.text
#                     w = w.replace(u'\xa0', u' ').replace(u'\u20b4', u'грн')
#                     char_value_list.append(w)
#         char_dict = dict(zip(char_name_list,char_value_list))
#         return char_dict
#     def get_char2():
#         char = soup2.find('section', class_='product__characteristics').find_all('ul', class_='option__list option__list--hide-content option__list--show-all')
#         char_name_list = []
#         char_value_list = []
#         for char_c in char:
#             for li in char_c.find_all('li', class_='option__item'):
#                 for span in li.find_all('span', class_='option__name--text'):
#                     char_name_list.append(span.text.strip(':\u2002'))
#                 for span in li.find_all('span', class_='option__value'):
#                     w = span.text
#                     w = w.replace(u'\xa0', u' ').replace(u'\u20b4', u'грн')
#                     char_value_list.append(w)
#         char_dict = dict(zip(char_name_list,char_value_list))
#         return char_dict
#
#     try:
#         products_dict['char'] = get_char()
#     except:
#         products_dict['char'] = get_char2()
#
#     return contents_dict

# def csv_record(items: dict, path: str) -> None:
#     with open(path, 'w', newline='') as f:
#         writer = csv.writer(f, delimiter=';')
#         writer.writerow(['Name','Photo','ART','Characteristics'])
#         for item in items:
#             try:
#                 writer.writerow([item['title'],item['img_link'],item['articul'],item['char']])
#             except:
#                 print('no data')
#                 continue
# def main() -> None:
#     products_list = []
#     groups = pars_URL(URL)
#     i = 1
#     for group in groups:
#         page_num = last_page(HOST+group)
#         #print(f"Количество продуктов: {len(get_list_links(page_num, HOST+group))}")
#         print(i)
#         i += 1
#         for response in get_response(page_num, HOST+group):
#             products_list.append(get_contents(response))
#     csv_record(products_list, CSV)
#     print('DONE')
# if __name__ == '__main__':
#     start_time = time.time()
#     start()
#     print("--- %s seconds ---" % (time.time() - start_time))