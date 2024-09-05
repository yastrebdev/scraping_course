import json
import re
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from elements.get import get_tags

ua = UserAgent().random

headers = {
    'User-Agent': ua
}

def get_data(file_path):
    count = 1

    with open(file_path, 'r', encoding='utf-8') as file:
        urls_list = [line.strip() for line in file.readlines()]

    session = requests.Session()

    posts_list = []
    for url in urls_list[:100]:
        other_urls_list = []

        response = session.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        post_content = None
        post_info = None

        try:
            post_content = soup.find('div', id='post')
        except Exception as _ex:
            print(_ex)
            print('================================')
            print('[INFO] Не нашли блок с ID "post" :(')

        if post_content:
            try:
                post_title = post_content.find('h1', class_='single-title').text.strip()
            except Exception as _ex:
                print(_ex)
                print('================================')
                print('[INFO] Не нашли блок с CLASS "single-title" :(')
                post_title = 'Untitled'

            try:
                post_info = post_content.find('div', class_='info')
            except Exception as _ex:
                print(_ex)
                print('================================')
                print('[INFO] Не нашли блок с CLASS "info" :(')

            if post_info:
                try:
                    post_author = post_info.find('a', class_='author').text.strip()
                except Exception as _ex:
                    print(_ex)
                    print('================================')
                    print('[INFO] Не нашли блок с CLASS "author" :(')
                    post_author = 'Аноним'

                try:
                    block_data = post_info.find('div', class_='post__date-inner')
                    if block_data:
                        post_date = block_data.find('time', class_='post__date').text.strip()
                    else:
                        post_date = post_info.find('time', class_='post__date').text.strip()
                except Exception as _ex:
                    print(_ex)
                    print('================================')
                    print('[INFO] Не нашли блок с CLASS "post__date" :(')
                    post_date = '00.00.0000'

            else:
                post_author = 'Аноним'
                post_date = '00.00.0000'

            try:
                post_theme = post_content.find('ol', class_='breadcrumbs').find_all('li')[-1].find('span').text.strip()
            except Exception as _ex:
                print(_ex)
                print('================================')
                print('[INFO] Не нашли блок с CLASS "breadcrumbs" :(')
                post_theme = 'Без темы'

            post_links = post_content.find('div', class_='text').find_all('a')
            post_source = post_content.find('div', class_='text').find_all('p')[-1].text

            links = []
            if post_source.count('Источник:'):
                links.append(post_source.split(': ')[1])

            for link in post_links:
                if isinstance(link, str):
                    other_urls_list.append(f'https://{link}')
                    continue

                url = link['href']
                if url[0] == '#' or re.search(r'hi-news|hinews', url):
                    continue
                else:
                    other_urls_list.append(url)

            post_tags_list = get_tags(block=post_content)

            posts_list.append(
                {
                    'title': post_title,
                    'url': url,
                    'author': post_author,
                    'date': post_date,
                    'theme': post_theme,
                    'links': other_urls_list,
                    'tags': post_tags_list,
                }
            )
        else:
            continue

        print(f'[+] Обработано постов {count}/100')
        count += 1

    with open('posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts_list, f, indent=4, ensure_ascii=False)

def main():
    start_time = time.time()
    get_data('article_urls.txt')
    finish_time = time.time() - start_time
    print(f'[SUCCESS] Сбор данных завершен за {time.strftime("%H:%M:%S", time.gmtime(finish_time))}')

if __name__ == '__main__':
    main()