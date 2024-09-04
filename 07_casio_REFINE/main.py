import json
import os
import requests
from fake_useragent import UserAgent

ua = UserAgent().random

def get_all_pages():
    headers = {
        'user-agent': ua
    }

    url = 'https://www.casio.com/content/casio/locales/intl/en/products/watches/gshock/jcr:content/root/responsivegrid/container/product_panel_list_f.products.json'

    res = requests.get(url=url, headers=headers)

    if not os.path.exists('data'):
        os.mkdir('data')

    # Сохраняем JSON-ответ в файл
    with open('data/page_1.json', 'w', encoding='utf-8') as file:
        file.write(res.text)

    # Загружаем JSON-данные из файла
    with open('data/page_1.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    models = data['data']

    for i in range(len(models)):
        product_name = models[i]['dataProductName']
        print(product_name)

def main():
    get_all_pages()

if __name__ == '__main__':
    main()