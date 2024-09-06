import json
import time
from datetime import datetime
import requests
import threading
from queue import Queue
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from elements.get import (
    get_tags,
    get_post_content,
    get_post_title,
    get_post_info,
    get_post_author,
    get_post_date,
    get_post_theme,
    get_post_other_urls
)


def process_url(*, url, session, result_queue):
    headers = {
        'User-Agent': UserAgent().random
    }
    response = session.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    post_content = get_post_content(block=soup)

    if post_content:
        post_title = get_post_title(block=post_content)
        post_info = get_post_info(block=post_content)

        if post_info:
            post_author = get_post_author(block=post_info)
            post_date = get_post_date(block=post_info)
        else:
            post_author = 'Аноним'
            post_date = '00.00.0000'

        post_theme = get_post_theme(block=post_content)
        other_urls_list = get_post_other_urls(block=post_content)
        post_tags_list = get_tags(block=post_content)

        result_queue.put({
            'title': post_title,
            'url': url,
            'author': post_author,
            'date': post_date,
            'theme': post_theme,
            'links': other_urls_list,
            'tags': post_tags_list,
        })
    else:
        result_queue.put(None)


def get_data(file_path):
    count = 1

    with open(file_path, 'r', encoding='utf-8') as file:
        urls_list = [line.strip() for line in file.readlines()]

    session = requests.Session()
    result_queue = Queue()
    threads = []

    for url in urls_list:
        thread = threading.Thread(target=process_url, kwargs={'url': url, 'session': session, 'result_queue': result_queue})
        threads.append(thread)
        thread.start()

        print(f'[+] Обработано постов {count}/{len(urls_list)}')
        count += 1

    for thread in threads:
        thread.join()

    posts_list = []
    while not result_queue.empty():
        result = result_queue.get()
        if result:
            posts_list.append(result)

    with open('posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts_list, f, indent=4, ensure_ascii=False)


def main():
    start_time = time.time()
    get_data('article_urls.txt')
    finish_time = time.time() - start_time
    print(f'[SUCCESS] Сбор данных завершен за {time.strftime("%H:%M:%S", time.gmtime(finish_time))}')

if __name__ == '__main__':
    main()