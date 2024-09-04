import json
from textwrap import indent

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent().random
headers = {
    'user-agent': ua
}

# person_urls = []
# for i in range(0, 760, 20):
#     url = f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=12&noFilterSet=true&offset={i}'
#
#     response = requests.get(url=url, headers=headers)
#     result = response.content
#
#     soup = BeautifulSoup(result, 'lxml')
#     persons = soup.find_all('div', class_='bt-slide-content')
#
#     for person in persons:
#         url = person.find('a')['href']
#         person_urls.append(url)
#
# with open('person_urls_list.txt', 'w', encoding='utf-8') as file:
#     for line in person_urls:
#         file.write(f'{line}\n')

with open('person_urls_list.txt') as file:
    lines = [line.strip() for line in file.readlines()]

    data_persons = []
    count = 0
    for line in lines:
        response = requests.get(url=line, headers=headers)
        result = response.content

        soup = BeautifulSoup(result, 'lxml')
        person = soup.find('div', class_='bt-biografie-name').find('h3').text
        person_name_company = person.strip().split(',')

        person_name = person_name_company[0]
        person_company = person_name_company[1].strip()

        social_networks = soup.find_all('a', class_='bt-link-extern')

        social_networks_urls = []
        for link in social_networks:
            social_networks_urls.append(link['href'])

        data = {
            'person_name': person_name,
            'person_company': person_company,
            'social_networks': social_networks_urls
        }

        print(f'#{count}: {line} is done')
        count += 1

        data_persons.append(data)

        with open('data_persons.json', 'w', encoding='utf-8') as json_file:
            json.dump(data_persons, json_file, indent=4, ensure_ascii=False)