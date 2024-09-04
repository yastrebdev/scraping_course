import json
import os
import time
from random import randrange
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from urllib.parse import unquote

ua = UserAgent().random

headers = {
    'user-agent': ua,
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
}

def get_source_html():
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={ua}')
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    pages_count = 34

    for page in range(1, pages_count + 1):
        url = f'https://zoon.ru/spb/medical/page-{page}'

        driver.get(url)
        time.sleep(randrange(5, 10))

        html_source = driver.page_source

        with open(f'pages/page-{page}.html', 'w', encoding='utf-8') as file:
            file.write(html_source)

        print(f'[+] Progress {page}/{pages_count}')

    driver.close()
    driver.quit()


def get_items_urls(file_path):
    sorted_pages = sorted(os.listdir(file_path), key=lambda x: int(x.split('-')[1].split('.')[0]))

    item_urls_list = []
    for html in sorted_pages:
        with open(f'{file_path}/{html}', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        cards_info = soup.find_all('div', class_='minicard-item__info')

        for item in cards_info:
            item_url = item.find('div', class_='minicard-item__title').find('a')['href']
            item_urls_list.append(item_url)

    with open('clinic_urls.txt', 'w', encoding='utf-8') as file:
        for url in item_urls_list:
            file.write(f'{url}\n')

    return '[INFO] Urls collected successfully!'


def get_data(file_path):
    with open(file_path, encoding='utf-8') as file:
        url_list = [url.strip() for url in file.readlines()]

    result_list = []
    count = 1
    pages_count = len(url_list)
    for url in url_list:
        res = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')

        try:
            item_name = soup.find('span', {'itemprop': 'name'}).text.strip()
        except Exception as _ex:
            item_name = None

        item_phone_list = []
        try:
            item_phones = soup.find('div', class_='service-phones-list').find_all('a', class_='js-phone-number')
            for phone in item_phones:
                item_phone = phone['href'].split(':')[-1].strip()
                item_phone_list.append(item_phone)
        except Exception as _ex:
            item_phone_list = None

        try:
            item_address = soup.find('address', class_='iblock').text.strip()
        except Exception as _ex:
            item_address = None

        try:
            item_site = soup.find('div', class_='service-website-value').find('a').text.strip()
        except Exception as _ex:
            item_site = None

        social_networks_list = []
        try:
            item_socials = soup.find('div', class_='service-description-social-list').find_all('a', class_='js-service-social')
            for link in item_socials:
                url = link['href']
                clear_url = unquote(url.split('?to=')[1].split('&')[0])
                social_networks_list.append(clear_url)

        except Exception as _ex:
            social_networks_list = None

        result_list.append({
            'name': item_name,
            'phones': item_phone_list,
            'address': item_address,
            'site': item_site,
            'social_networks': social_networks_list
        })

        time.sleep(randrange(2, 5))
        if count % 10 == 0:
            time.sleep(randrange(5, 9))

        print(f'[+] Processed: {count}/{pages_count} pages...')

        count += 1

    with open('clinic.json', 'w', encoding='utf-8') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)

    return '[INFO] Data collected successfully!'

def main():
    # get_source_html()
    # print(get_items_urls('pages'))
    start_time = time.time()
    print(get_data('clinic_urls.txt'))
    finish_time = time.time() - start_time
    print(f'Worked time: {finish_time}')


if __name__ == '__main__':
    main()