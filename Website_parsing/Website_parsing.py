import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cards.csv'
HOST = 'https://minfin.com.ua/'
urls = [
    'https://minfin.com.ua/cards/credit/',
    'https://minfin.com.ua/cards/debit/'
]
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}


def get_html(url, params=''):
    req = requests.get(url, headers=HEADERS, params=params)
    return req


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='sc-182gfyr-0 jmBHNg')
    cards = []
    for item in items:
        cards.append(
            {
                'title': item.find('a', class_='cpshbz-0 eRamNS').get_text(strip=True),
                'product_link': HOST + item.find('a', class_='cpshbz-0 eRamNS').get('href'),
                'brand': item.find('div', class_='be80pr-16 be80pr-17 kpDSWu cxzlon').find('span').get_text(strip=True),
                'card_img': item.find('div', class_='be80pr-9 fJFiLL').find('img').get('src')
            }
        )
    return cards


def get_cards_type_name(html1):
    soup1 = BeautifulSoup(html1, 'html.parser')
    cards_type = soup1.find('h1', class_='sc-3dg7pc-3 jUjTJy').get_text(strip=True)
    return cards_type


def save_results_to_csv(items, path):
    with open(path, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Product name', 'Product link', 'Bank name', 'Image link'])
        for item in items:
            writer.writerow([item['title'], item['product_link'], item['brand'], item['brand'], item['card_img']])


def parser():
    cards = []
    for URL in urls:
        html = get_html(URL)
        if html.status_code == 200:
            print(get_cards_type_name(html.text))
            cards.extend(get_content(html.text))
            print(cards)
        else:
            print('Error! -> ' + URL)
            break
    save_results_to_csv(cards, CSV)


parser()

# Do not forget to read README.md file
