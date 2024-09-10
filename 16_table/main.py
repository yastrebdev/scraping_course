import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from proxy_config import login, password, proxy
requests.packages.urllib3.disable_warnings()

headers = {
    'User-Agent': UserAgent().random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
}

proxies = {
    'https': f'http://{login}:{password}@{proxy}'
}

def get_data(url):
    cur_data = datetime.now().strftime('%m_%d_%Y')
    # response = requests.get(url=url, headers=headers, proxies=proxies)

    # with open(file='index.html', mode='w', encoding='utf-8') as file:
    #     file.write(response.text)

    with open(file='index.html') as file:
        src = file.read()

    soup = BeautifulSoup(markup=src, features='lxml')
    table = soup.find('table', id='ro5xgenergy')

    data_th = table.find('thead').find_all('tr')[-1].find_all('th')
    table_headers = ['Area']
    for dth in data_th:
        dth = dth.text.strip()
        table_headers.append(dth)

    with open(file=f'data_{cur_data}.csv', mode='w', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                table_headers
            )
        )

    tbody_trs = table.find('tbody').find_all('tr')

    ids = []
    data = []
    for tr in tbody_trs:
        area = tr.find('th').text.strip()

        data_by_month = tr.find_all('td')
        data = [area]
        for dbm in data_by_month:
            if dbm.find('a'):
                area_data = dbm.find('a')['href']
                id = area_data.split('/')[4].split('?')[0]
                ids.append(id)
            elif dbm.find('span'):
                area_data = dbm.find('span').text.strip()
            else:
                area_data = None

            data.append(area_data)

        with open(file=f'data_{cur_data}.csv', mode='a', encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                    data
                )
            )

    with open(file='ids.txt', mode='w', encoding='utf-8') as file:
        for id in ids:
            file.write(f'{id}\n')

    return 'Work completed!'


def download_xlsx(file_path='ids.txt'):

    with open(file=file_path) as file:
        ids = [line.strip() for line in file.readlines()]

    for i, id in enumerate(ids):
        headers = {
            'Host': 'data.bls.gov',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Accept-Language': 'ru-RU',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
            'Origin': 'https://data.bls.gov',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Priority': 'u=0, i',
            'Connection': 'keep-alive',
        }

        data = {
            'request_action': 'get_data',
            'reformat': 'true',
            'from_results_page': 'true',
            'years_option': 'specific_years',
            'delimiter': 'comma',
            'output_type': 'multi',
            'periods_option': 'all_periods',
            'output_view': 'data',
            'output_format': 'excelTable',
            'original_output_type': 'default',
            'annualAveragesRequested': 'false',
            'series_id': id,
        }

        response = requests.post('https://data.bls.gov/pdq/SurveyOutputServlet', headers=headers,
                                 data=data, verify=False, proxies=proxies)

        with open(file=f'xlsx_files/{id}.xlsx', mode='wb') as file:
            file.write(response.content)

        print(f'{i + 1}/{len(ids)}')


def main():
    # print(get_data(url='https://www.bls.gov/regions/midwest/data/AverageEnergyPrices_SelectedAreas_Table.htm'))
    download_xlsx()

if __name__ == '__main__':
    main()