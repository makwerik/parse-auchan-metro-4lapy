import csv

import requests
from bs4 import BeautifulSoup


class MetroParse:
    """Парсим шоколадки. Магазин - Метро"""

    def __init__(self, page=1):
        """Инициализируем кол-во страниц, которые нужно спарсить"""
        self.page = page

    def get_data(self):
        print('Начинаем парсить')
        for p in range(1, self.page + 1):
            response = requests.get(
                f'https://online.metro-cc.ru/category/sladosti-chipsy-sneki/shokolad-batonchiki?page={p}').text

            soup = BeautifulSoup(response, 'lxml')
            content = soup.find_all(
                class_='catalog-2-level-product-card product-card subcategory-or-type__products-item with-prices-drop')

            for c in content:
                itemsID = c.get('data-sku')
                name = c.find(class_='product-card-name__text').text
                link = f"https://online.metro-cc.ru{c.find('a').get('href')}"
                regular_price = c.find(class_='product-price__sum-rubles').text

                if regular_price.isdigit():
                    regular_price = regular_price
                else:
                    regular_price = 'Доступен только в магазине или отсутствует'
                try:
                    sales = c.find_all(class_='product-price__sum-rubles')[1].text
                    if sales.isdigit():
                        sales = sales
                    else:
                        sales = 'Доступен только в магазине или отсутствует'
                except:
                    sales = ''

                get_brand = requests.get(link).text
                soup_brand = BeautifulSoup(get_brand, 'lxml'). \
                    find_all(class_='product-attributes__list-item-link')[3].text

                data = {"itemsID": itemsID, "name": name.strip(), "link": link, "regular_price": regular_price.strip(),
                        "sales": sales.strip(), "soup_brand": soup_brand.strip()}
                self.whrite_csv(data)

    @staticmethod
    def whrite_csv(data):
        with open("data_metro.csv", mode="a", encoding='utf8') as w_file:
            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
            file_writer.writerow([data['itemsID'], data['name'],
                                  data['link'], data['regular_price'],
                                  data['sales'], data['soup_brand']])


if __name__ == '__main__':
    m = MetroParse()
    m.get_data()
