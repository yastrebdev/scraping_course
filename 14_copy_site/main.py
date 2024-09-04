import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent().random

headers = {
    'User-Agent': ua
}

pagination_count = 4554

def get_articles_urls(url):
    session = requests.Session()
    response = session.get(url=url, headers=headers)

    articles_urls_list = []
    for page in range(1, pagination_count + 1):
        url = f'https://hi-news.ru/page/{page}'
        response = session.get(url=url, headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')

        article_links = soup.find_all('h2', class_='post__title')

        for link in article_links:
            url = link.find('a')['href']
            articles_urls_list.append(url)

        print(f'[+] Обработал {page}/{pagination_count}')

    with open('article_urls.txt', 'w', encoding='utf-8') as file:
        for url in articles_urls_list:
            file.write(f'{url}\n')


def main():
    get_articles_urls(url='https://hi-news.ru/')


if __name__ == '__main__':
    main()