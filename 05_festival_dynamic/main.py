import json
import time
from selenium.webdriver.support import expected_conditions as EC

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

ua = UserAgent().random

headers = {
    'user-agent': ua
}

card_urls_list = []
for i in range(0, 192, 24):
    # url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=30%20Aug%202024&to_date=&maxprice=500&o={i}&bannertitle=September'
    #
    # response = requests.get(url=url, headers=headers)
    # json_data = json.loads(response.text)
    # html_response = json_data['html']
    #
    # with open(f'data/index_{i}.html', 'w', encoding='utf-8') as file:
    #     file.write(html_response)

    with open(f'data/index_{i}.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    card_links = soup.find_all('a', class_='card-img-link')

    for link in card_links:
        url = link['href']
        card_urls_list.append(f'https://www.skiddle.com{url}')

fest_list_result = []
for url in card_urls_list:
    location_url = ''

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    time.sleep(3)

    try:
        iframe_block = driver.find_element(By.CLASS_NAME, "css-zzbvj8")

        if iframe_block is None:
            continue

        ActionChains(driver) \
            .scroll_to_element(iframe_block) \
            .perform()

        if iframe_block.is_displayed():

            iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
            )

            iframe_src = iframe.get_attribute('src')
            location_url = iframe_src

    except Exception as _ex:
        print(f'Произошла ошибка на {url}: {_ex}')

    response = requests.get(url=url, headers=headers)

    try:
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('h1').text

        date_block = soup.find('div', class_='css-twt0ol')
        date_spans = date_block.find_all('span')
        full_date = date_spans[0].text + date_spans[1].text

        # location_url = soup.find('iframe')

        print(title)
        print(full_date)
        print(location_url)
        print('#'*20)

        fest_list_result.append(
            {
                'title': title,
                'date': full_date,
                'location_url': location_url
            }
        )

    except Exception as _ex:
        print(_ex)
        print('Damn... There was same error...')

    driver.close()
    driver.quit()

with open('data/data.json', 'a', encoding='utf-8') as file:
    json.dump(fest_list_result, file, indent=4, sort_keys=False)