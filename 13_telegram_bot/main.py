import json
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent().random

headers = {
    'User-Agent': ua,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
}

def get_page(url):
    session = requests.Session()
    response = session.get(url=url, headers=headers)

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(response.text)


def collect_data():
    with open('index.html', 'r', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    pagination = soup.find('div', class_='paging').find_all('td')[1]
    page_count = int(len(pagination.find_all('a')) - 1)

    result_data = []
    for i in range(1, page_count + 1):
        url = f'https://trial-sport.ru/gds.php?s=761611&c1=1070485&c2[]=1070486&discount=1&sizes[]=44.5&sizes[]=45.0&gender[]=1070482&gpp=100&pg={i}'

        session = requests.Session()
        response = session.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        products_block = soup.find('div', class_='right_col').find('div', class_='objects')
        products_list = products_block.find_all('div', class_='object')

        for shoes in products_list:
            screen = shoes.find('div', class_='img')
            discount = screen.find('i', class_='percent')
            if not discount is None:
                shoes_info = shoes.find('span', class_='txt')
                link = shoes_info.find('a', class_='title')
                brand = shoes_info.find('span', class_='brand_collection').find('span', class_='blue').text
                base_price = shoes_info.find('span', class_='price').find('span', class_='value').text.replace("\u2009", '')
                discount_price = shoes_info.find('span', class_='discount').find('span', class_='value').text.replace("\u2009", '')

                shoes_object = {
                    'title': link['title'],
                    'url': f'https://trial-sport.ru{link['href']}',
                    'brand': brand,
                    'base_price': base_price,
                    'discount_price': discount_price
                }

                percent = int(discount.text.replace('%', ''))
                if percent >= 50:
                    result_data.append(shoes_object)

    with open('shoes.json', 'w', encoding='utf-8') as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)

def main():
    # get_page(url='https://trial-sport.ru/gds.php?change_price=&s=761611&gpp=100&c1=1070485&discount=1&c2%5B%5D=1070486&price_from=&price_to=&sizes%5B%5D=44.5&sizes%5B%5D=45.0&sort=0')
    collect_data()


if __name__ == '__main__':
    main()