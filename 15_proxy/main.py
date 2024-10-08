import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

login = 'ztxpzN'
password = '1500TL'

ua = UserAgent().random

headers = {
    'User-Agent': ua
}

proxies = {
    'http': f'http://{login}:{password}@191.102.147.25:8000'
}

def get_location(*, url):
    response = requests.get(url=url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(response.text, 'lxml')

    ip = soup.find('div', class_='ip').text.strip()
    location = soup.find('div', class_='value-country').text.strip()

    print(ip)
    print(location)

def main():
    get_location(url='http://2ip.ru')

if __name__ == '__main__':
    main()