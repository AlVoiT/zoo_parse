import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import csv
import time


CSV = 'DATA.csv'
HOST = 'https://www.zooplus.de'
URL = 'https://www.zooplus.de/tierarzt/results'
params = {'animal_99': 'true', 'page': '1'}

session = requests.Session()
y = session.get('https://www.zooplus.de/tierarzt/api/v2/token?debug=authReduxMiddleware-tokenIsExpired')
t = (y.text).split(':')[1].strip('}').strip('"')
headers = {'accept': 'application/json',
           'authorization': f'Bearer {t}'
           }
print(headers)
r = session.get('https://www.zooplus.de/tierarzt/api/v2/results?animal_99=true&page=1&from=0&size=20', headers=headers)

gg = (r.json()['results'][0])
gg = dict(gg)
gg = gg['email']
print(gg)


# with open('test.json', 'w') as f:
#     f.write(str(r.headers))
#     f.write('______')
#     f.write(str(r.cookies))
#     f.write('______')
#     f.write(str(r.url))

def get_html(url: str, headers: dict, params: dict, cookies: dict) -> 'bs4.BeautifulSoup':
    response = requests.get(url, headers=headers, params=params, cookies=cookies)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

#print(BeautifulSoup(requests.get(URL).text, 'lxml'))