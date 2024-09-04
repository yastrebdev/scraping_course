import json
from datetime import datetime

import requests
from fake_useragent import UserAgent

ua = UserAgent().random

def get_data():
    start_time = datetime.now()

    headers = {
        'User-Agent': ua,
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': '*/*'
    }

    url = 'https://roscarservis.ru/catalog/legkovye/?set_filter=Y&sort%5Bprice%5D=asc&PAGEN_1=1'
    res = requests.get(url=url, headers=headers)

    # with open('data.json', 'w') as file:
    #    json.dump(res.json(), file, indent=4, ensure_ascii=False)

    page_count = res.json()['pagesCount']

    data_list = []
    for page in range(1, page_count + 1):
        url = f'https://roscarservis.ru/catalog/legkovye/?set_filter=Y&sort%5Bprice%5D=asc&PAGEN_1={page}'
        res = requests.get(url=url, headers=headers)
        data = res.json()
        items = data['items']

        possible_stores = ['discountStores', 'externalStores', 'commonStores']
        for item in items:
            total_amount = 0

            item_name = item['name']
            item_price = item['price']
            item_img = f'https://roscarservis.ru{item['imgSrc']}'
            item_url = f'https://roscarservis.ru{item['url']}'

            stores = []
            for ps in possible_stores:
                if ps in item:
                    if item[ps] is None or len(item[ps]) < 1:
                        continue
                    else:
                        for store in item[ps]:
                            store_name = store['STORE_NAME']
                            store_price = store['PRICE']
                            store_amount = store['AMOUNT']
                            total_amount += int(store['AMOUNT'])
                            stores.append(
                                {
                                    'store_name': store_name,
                                    'store_price': store_price,
                                    'store_amount': store_amount,
                                }
                            )

            data_list.append(
                {
                    'name': item_name,
                    'price': item_price,
                    'img_url': item_img,
                    'url': item_url,
                    'stores': stores,
                    'total_amount': total_amount
                }
            )

        print(f'[INFO] Обработал {page}/{page_count}')

    cur_time = datetime.now().strftime('%d_%m_%Y_%H_%M')
    with open(f'data_{cur_time}.json', 'a', encoding='utf-8') as file:
        json.dump(data_list, file, indent=4, ensure_ascii=False)

    diff_time = datetime.now() - start_time
    print(diff_time)

def main():
    get_data()

if __name__ == '__main__':
    main()