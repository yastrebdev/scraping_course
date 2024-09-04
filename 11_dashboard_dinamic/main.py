import json
import os
import time

import requests
from fake_useragent import UserAgent

ua = UserAgent().random

hs = {
    'User-Agent': ua,
    'Accept': '*/*'
}


def get_data_file(headers):
    # url = 'https://www.landingfolio.com/'
    # res = requests.get(url=url, headers=headers)
    #
    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(res.text)

    page = 1
    img_count = 0
    result_list = []
    while True:
        url = f'https://s3.landingfolio.com/inspiration?page={page}&sortBy=free-first'

        res = requests.get(url=url, headers=headers)
        data = res.json()

        for item in data:

            images = []
            for screen in item['screenshots']:
                images.append(
                    {
                        'title': screen['title'],
                        'desktop': f'https://landingfoliocom.imgix.net/{screen['images']['desktop']}',
                        'mobile': f'https://landingfoliocom.imgix.net/{screen['images']['mobile']}'
                    }
                )

                if screen['images']['mobile']:
                    img_count += 2
                else:
                    img_count += 1

            if 'screenshots' in item:
                result_list.append(
                    {
                        'title': item['title'].strip(),
                        'url': item['url'],
                        'images': images
                    }
                )

        if not data:
            break
        print(f'[+] Processed {page}')
        page += 1

    with open('data.json', 'w') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)
    return f'[INFO] Work finished. Images count is {img_count}'


def download_images(file_path):
    try:
        with open(file_path) as file:
            src = json.load(file)
    except Exception as _ex:
        print(_ex)
        return '[INFO] Check the file path!'

    items_len = len(src)
    count = 1

    for item in src[:100]:
        item_name = item['title']
        item_images = item['images']

        if not os.path.exists(f'data/{item_name}'):
            os.mkdir(f'data/{item_name}')

        for img in item_images:
            res_desktop = requests.get(url=img['desktop'])

            with open(f'data/{item_name}/desktop_{img['title']}.png', 'wb') as file:
                file.write(res_desktop.content)

            res_mobile = requests.get(url=img['mobile'])

            with open(f'data/{item_name}/mobile_{img['title']}.png', 'wb') as file:
                file.write(res_mobile.content)

            print(f'[+] Download {count}/{items_len}')
            count += 1

    return '[INFO] work finished!'


def main():
    start_time = time.time()
    # print(get_data_file(hs))
    print(download_images('data.json'))
    finish_time = time.time() - start_time

    print(f'Worked time: {finish_time}')


if __name__ == '__main__':
    main()