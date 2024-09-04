import requests
from fake_useragent import UserAgent
import img2pdf

ua = UserAgent().random

def get_data():
    headers = {
        'Accept': 'image/avif,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': ua
    }

    img_list = []
    for i in range(1, 49):
        url = f'https://www.recordpower.co.uk/flip/Winter2020/files/mobile/{i}.jpg'

        response = requests.get(url=url, headers=headers).content

        with open(f'media/{i}.jpg', 'wb') as file:
            file.write(response)
            img_list.append(f'media/{i}.jpg')
            print(f'Downloaded {i} of 48')

    print('#' * 20)
    print(img_list)

    # create PDF
    with open('result.pdf', 'wb') as f:
        f.write(img2pdf.convert(img_list))

def main():
    get_data()

if __name__ == '__main__':
    main()