import urllib.request
from urllib.error import URLError
import requests
from bs4 import BeautifulSoup
import argparse
import os


def get_image_from_google(url, directory):
    # url = "https://www.google.co.in/search?q="+name+"&source=lnms&tbm=isch"
    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }

    params = {
        "q": url,
        "tbm": "isch",
        "source": "lnms",
    }

    html = requests.get("https://www.google.com/search", params=params, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    img_list = soup.find_all('img')
    if not os.path.exists(directory):
        os.makedirs(directory)
    for index, image in enumerate(img_list[:16]):
        src = image['src']
        if 'https://encrypted-tbn0.gstatic.com/images?q=tbn:' in src:
            try:
                urllib.request.urlretrieve(src, f'{directory}/{index}.jpg')
            except URLError as e:
                print(f'Не удалось скачать изображение: {src}. \n {e}')

    print('Download complete')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Введите запрос по которому вы хотите скачать изображения", type=str)
    args = parser.parse_args()
    directory = args.url + '/'
    get_image_from_google(args.url, directory)
