import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent().random

h = {
    'user-agent': ua
}

def test_request(*, url, headers, retry=5):
    try:
        response = requests.get(url=url, headers=headers)
        print(f'[+] {url} {response.status_code}')
    except Exception as ex:
        if retry:
            print(f'[INFO] retry={retry} => {url}')
            return test_request(url=url, headers=headers, retry=retry - 1)
        else:
            raise
    else: return response

def main():
    pass

if __name__ == '__main__':
    main()