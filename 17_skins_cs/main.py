import requests
import json
from fake_useragent import UserAgent

ua = UserAgent().random
headers = {
    'User-Agent': ua
}

categories = {
    'ножи': 2,
    'штурмовые винтовки': 3
}


def collect_data(*, category = 'штурмовые винтовки', discount = 10):
    offset = 0
    batch_size = 60
    count = 1

    items_list = []
    while True:
        url = f'https://cs.money/1.0/market/sell-orders?limit=60&offset={offset}&type={categories[category]}'
        response = requests.get(url=url, headers=headers)
        if 'errors' in response.json():
            break

        data = response.json()
        items = data['items']

        for item in items:
            if int(item['pricing']['discount'] * 100) >= discount:
                item_id = item['id']
                item_full_name = item['asset']['names']['full']
                try:
                    item_3d = item['links']['3d']
                except Exception as _ex:
                    print('[WAR] No "item_3d"')
                    item_3d = 'Нет ссылки'
                item_images = item['asset']['images']
                item_price = item['pricing']['computed']
                item_discount = int(item['pricing']['discount'] * 100)

                items_list.append(
                    {
                        'id': item_id,
                        'full_name': item_full_name,
                        '3d_link': item_3d,
                        'images': item_images,
                        'price': item_price,
                        'discount': item_discount
                    }
                )

        offset += batch_size
        print(f'[+] PAGE -- {count}')
        count += 1


    print(f'[COMPLETE] Items count = {len(items_list)}')

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(items_list, file, indent=4, ensure_ascii=False)


def main():
    collect_data()


if __name__ == '__main__':
    main()