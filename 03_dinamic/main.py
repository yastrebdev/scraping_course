import json
import os
import time
import random
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent().random

base_url = 'https://scrapingclub.com'

def get_data(*, url):
    headers = {
        'user-agent': ua,
    }

    product_data_list = []
    iteration_count = 5
    print(f'Всего итераций: #{iteration_count}')

    for i in range(1, 6):
        res = requests.get(url=f'{base_url}/exercise/list_infinite_scroll/?page={i}', headers=headers)

        folder_name = f'data/data_{i}'

        if os.path.exists(folder_name):
            print('Folder is true')
        else:
            os.mkdir(folder_name)

        with open(f'{folder_name}/page_{i}.html', 'w', encoding='utf-8') as file:
            file.write(res.text)

        with open(f'{folder_name}/page_{i}.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        cards = soup.find_all('div', class_='post')

        product_urls = []
        for card in cards:
            link = f'{base_url}{card.find('a')['href']}'
            product_urls.append(link)

        for product_url in product_urls:
            res = requests.get(product_url, headers=headers)
            product_name = product_url.split('/')[-2]

            with open(f'{folder_name}/{product_name}.html', 'w', encoding='utf-8') as file:
                file.write(res.text)

            with open(f'{folder_name}/{product_name}.html') as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')
            product_card = soup.find('div', class_='my-8')

            try:
                product_img = f'{base_url}{product_card.find('div').find('img', class_='card-img-top')['src']}'
            except Exception:
                product_img = 'No product img'

            product_info = product_card.find('div', class_='p-6')

            try:
                product_name = product_info.find('h3', class_='card-title').text
            except Exception:
                product_name = 'No product name'

            try:
                product_price = product_info.find('h4', class_='card-price').text
            except Exception:
                product_price = 'No product price'

            try:
                product_description = product_info.find('p', class_='card-description').text
            except Exception:
                product_description = 'No product description'

            product_data_list.append(
                {
                    'img': product_img,
                    'name': product_name,
                    'price': product_price,
                    'description': product_description
                }
            )

        iteration_count -= 1
        print(f'Осталось итераций: #{iteration_count}')
        if iteration_count == 0:
            print('Сбор завершен')

        time.sleep(random.randrange(2, 4))

    with open('data/product_data.json', 'a', encoding='utf-8') as file:
        json.dump(product_data_list, file, indent=4, ensure_ascii=False)

def main():
    get_data(url = base_url)

if __name__ == '__main__':
    main()