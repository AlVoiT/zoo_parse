from __future__ import annotations
import argparse
import sys
import requests
import csv
import time


def get_api_data(page: int, size: int) -> list:
    """
    Sends a GET request with token for getting API data.

    :param page: number of page parse.
    :param size: the number of hits to return.
    :return: list object.
    """
    session = requests.Session()
    token_response = session.get('https://www.zooplus.de/tierarzt/api/v2/token?debug=authReduxMiddleware-tokenIsExpired')
    token = token_response.json()['token']
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {token}'
    }
    params = {
        'animal_99': 'true',
        'page': str(page),
        'from': '0',
        'size': str(size)
    }
    response = session.get('https://www.zooplus.de/tierarzt/api/v2/results', headers=headers, params=params)
    api_data = response.json()['results']
    return api_data


def clear_data(data: list, field: list) -> list:
    """
    Clear data from API request.

    :param data: data from API request.
    :param field: list of columns for CSV headers.
    :return: list object.
    """
    clean_data = []
    for item in data:
        row = {key: value for key, value in item.items() if key in field}
        clean_data.append(row)
    return clean_data


def csv_header(field: list, path: str | None = 'example.csv') -> None:
    """
    Write headers to CSV file.

    :param field: list of columns for CSV headers.
    :param path: path to CSV file.
    :return: None
    """
    with open(path, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field)
        writer.writeheader()


def csv_record(item: dict, field: list, path: str | None = 'example.csv') -> None:
    """
    Record data to CSV file.

    :param item: dict from clean data (row for CSV file).
    :param field: list of columns for CSV headers.
    :param path: path to CSV file.
    :return: None
    """
    with open(path, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field)
        writer.writerow(item)


def main(args):
    size = args.page * 20
    api_data = get_api_data(page=args.page, size=size)
    clean_data = clear_data(data=api_data, field=args.headers)
    csv_header(field=args.headers, path=args.path)
    for row in clean_data:
        csv_record(item=row, field=args.headers, path=args.path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                                    description='Script receive data from zooplus API.',
                                    usage='python get_zooplus_data.py --headers {name, city, ...} --page 3'
                                          '--path data.csv'
    )
    parser.add_argument(
        '--headers',
        nargs='+',
        default=['name', 'address', 'city', 'telefon', 'count_reviews', 'avg_review_score'],
        choices=[
            'address', 'behandlung', 'brands_txt', 'brand_others_txt', 'breadcrumb', 'count_reviews',
            'avg_review_score', 'city', 'city_slug_txt', 'id', 'is_profile_linked', 'keywords', 'lat',
            'lng', 'location', 'name', 'open_time', 'paymentmethods_txt', 'parkingoptions_txt',
            'profile_image', 'schwerpunkt', 'reviews_nest', 'slug', 'telefon', 'wheelchair_accessible_txt',
            'zip', '_last_index_update_date'
        ],
        help='List for the headers of CSV file'
    )
    parser.add_argument(
        '--page',
        type=int,
        default=3,
        help='Number of pages to parse'
    )
    parser.add_argument(
        '--path',
        type=str,
        default='DATA.csv',
        help='Path to CSV file'
    )
    args = parser.parse_args(sys.argv[1:])
    start_time = time.time()
    main(args)
    print("--- %s seconds ---" % (time.time() - start_time))
