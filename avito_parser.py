import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def get_html(url):
    r = requests.get(url)
    return r.text


def find_max_page(url):
    html = get_html(url)

    soup = BeautifulSoup(html, 'html.parser')

    pages = soup.find('div', class_='pagination-root-2oCjZ').find_all('span', class_='pagination-item-1WyVp')
    max_page = pages[-2]['data-marker']

    return re.findall('(\d+)', max_page)[0]


def parse_page(search, page):
    website_url = "https://www.avito.ru"
    url = "https://www.avito.ru/moskva?q={0}".format(search)

    max_page = int(find_max_page(url))

    if max_page < page:
        print("Запрашиваемя страница больше максимально доступной, всего {0} страниц".format(max_page))
        return

    url = "https://www.avito.ru/moskva?q={0}&p={1}".format(search, page)
    print(url)

    html = get_html(url)

    soup = BeautifulSoup(html, 'html.parser')
    catalog = soup.find('div', class_='items-items-38oUm').find_all('div', class_='item_table')

    df = pd.DataFrame(columns=('title', 'price', 'url', 'metro', 'metro distance'))

    for product in catalog:

        try:
            title = product.find('div', class_='description').find('h3').text.strip()
        except:
            title = None

        try:
            product_url = product.find('div', class_='description').find('h3').find('a').get('href')
        except:
            product_url = None

        try:
            price = product.find('div', class_='description').find('div', class_='snippet-price-row').text.strip()
        except:
            price = None

        try:
            metro = product.find('div', class_='description').find('span',
                                                                   class_='item-address-georeferences-item__content').text.strip()
        except:
            metro = None

        try:
            distance_from_metro = product.find('div', class_='description').find('span',
                                                                                 class_='item-address-georeferences-item__after').text.strip()
        except:
            distance_from_metro = None

        df.loc[len(df)] = [title, price, website_url + product_url, metro, distance_from_metro]

    df.to_csv("Data", index=False)  # сохранили файл в csv формате
    print(df)
    return df


def main():
    print("Что ищем? ")
    request = str(input())
    print("Какую страницу поиска показать? ")
    page = int(input())

    data = parse_page(request, page)


if __name__ == '__main__':
    main()
