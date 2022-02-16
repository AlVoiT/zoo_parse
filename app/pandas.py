from __future__ import annotations
import requests
import pandas as pd
import time


CSV = 'DATA2.csv'
PAGE = 3


def get_api_data(page: int, count: int) -> list:

    session = requests.Session()
    token_resp = session.get('https://www.zooplus.de/tierarzt/api/v2/token?debug=authReduxMiddleware-tokenIsExpired')
    token = token_resp.json()['token']
    headers = {'accept': 'application/json',
               'authorization': f'Bearer {token}'
               }
    params = {'animal_99': 'true', 'page': str(page), 'from': str(count), 'size': '20'}
    resp = session.get('https://www.zooplus.de/tierarzt/api/v2/results', headers=headers, params=params)
    api_data = resp.json()['results']
    return api_data


def create_df(page: int) -> pd.DataFrame:

    items = []
    for pg in range(1, page+1):
        size = pg * 20
        count = range(0, size + 1, 20)[pg-1]
        data = get_api_data(pg, count)
        for item in data:
            items.append(item)
    df = pd.DataFrame(items)
    return df


def main():

    create_df(3).to_csv(CSV, index=False)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
