from __future__ import annotations

import requests
import pandas as pd
import csv
import time

CSV = 'DATA.csv'
HOST = 'https://www.zooplus.de'
URL = 'https://www.zooplus.de/tierarzt/results'
page = 1
params = {'animal_99': 'true', 'page': str(page)}

session = requests.Session()
token = session.get('https://www.zooplus.de/tierarzt/api/v2/token?debug=authReduxMiddleware-tokenIsExpired')
t = token.text.split(':')[1].strip('}').strip('"')
headers = {'accept': 'application/json',
           'authorization': f'Bearer {t}'
           }
print(headers)
r = session.get('https://www.zooplus.de/tierarzt/api/v2/results', headers=headers, params=params)

gg = (r.json()['results'])
lol = []
for i in gg:
    for y in dict(i).keys():
        lol.append(y)
# importing the module
import collections

# using Counter to find frequency of elements
frequency = collections.Counter(lol)

# printing the frequency
data = [key for key, value in dict(frequency).items() if value == 20]
print(data)



df = pd.DataFrame.from_dict(gg)
columns = ['address', 'behandlung', 'brands_txt', 'brand_others_txt', 'breadcrumb', 'count_reviews', \
           'avg_review_score', 'city', 'city_slug_txt', 'id', 'is_profile_linked', 'keywords', 'lat', \
           'lng', 'location', 'name', 'open_time', 'paymentmethods_txt', 'parkingoptions_txt', \
           'profile_image', 'schwerpunkt', 'reviews_nest', 'slug', 'telefon', 'wheelchair_accessible_txt', \
           'zip', '_last_index_update_date'
           ]


def csv_record(row: dict, columns: list, path: str | None = 'DATA.csv') -> None:
    with open(path, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writerow(row)


for i in gg:
    row = {k: v if isinstance(v, str) else v for k, v in i.items() if k in columns }
    csv_record(row, columns)



