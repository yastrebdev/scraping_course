import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent().random

def get_data():
    url = 'https://www.labirint.ru/genres/2308/?page=1'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'User-Agent': ua,
        'Referer': 'https://yandex.ru/'
    }

    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    pages_count = int(soup.find('div', class_='pagination-number').find_all('a')[-1].text)

    for page in range(2, 3):
        url = f'https://www.labirint.ru/genres/2308/?page={page}'
        res = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')

        books_items = soup.find('div', class_='products-row').find_all('div', class_='product')

        for card in books_items:
            books_item = card.find_all('div')

            try:
                book_title = books_item[0].find('a', class_='product-title-link').find('span').text
                print(book_title)
            except:
                print('No title')

def main():
    get_data()

if __name__ == '__main__':
    main()