from __future__ import annotations
import requests
import csv
import time


CSV = 'DATA.csv'
PAGE = 3
COLUMNS = ['address', 'behandlung', 'brands_txt', 'brand_others_txt', 'breadcrumb', 'count_reviews', \
           'avg_review_score', 'city', 'city_slug_txt', 'id', 'is_profile_linked', 'keywords', 'lat', \
           'lng', 'location', 'name', 'open_time', 'paymentmethods_txt', 'parkingoptions_txt', \
           'profile_image', 'schwerpunkt', 'reviews_nest', 'slug', 'telefon', 'wheelchair_accessible_txt', \
           'zip', '_last_index_update_date'
           ]


def get_api_data(page: int, columns: list) -> list:

    session = requests.Session()
    token_resp = session.get('https://www.zooplus.de/tierarzt/api/v2/token?debug=authReduxMiddleware-tokenIsExpired')
    token = token_resp.json()['token']
    headers = {'accept': 'application/json',
               'authorization': f'Bearer {token}'
               }
    params = {'animal_99': 'true', 'page': str(page)}
    resp = session.get('https://www.zooplus.de/tierarzt/api/v2/results', headers=headers, params=params)
    api_data = resp.json()['results']

    def extract_data(data: list, field: list) -> list:
        new_data = []
        for item in data:
            row = {key: value for key, value in item.items() if key in field}
            new_data.append(row)
        return new_data

    clean_data = extract_data(data=api_data, field=columns)
    return clean_data


def csv_header(field: list, path: str | None = 'example.csv') -> None:

    with open(path, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field)
        writer.writeheader()


def csv_record(item: dict, field: list, path: str | None = 'example.csv') -> None:

    with open(path, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field)
        writer.writerow(item)


def main():
    csv_header(field=COLUMNS, path=CSV)
    for page in range(1, PAGE+1):
        data = get_api_data(page=page, columns=COLUMNS)
        for row in data:
            csv_record(item=row, field=COLUMNS, path=CSV)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
