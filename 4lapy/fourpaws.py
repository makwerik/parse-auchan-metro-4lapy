import csv
import re
import requests
import json
import codecs

from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class FourPawsParse:
    """Парсим 4 лапы"""

    def __init__(self, page=2):
        """Инициализируем кол-во страниц и хедерс"""
        agent = UserAgent()
        self.page = page

        self.headers = {
            'authority': '4lapy.ru',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'ru,en;q=0.9',
            # 'cookie': 'rrpvid=447139764624440; _gcl_au=1.1.438860711.1711744229; PHPSESSID=6n60kkc899eem77ueifhdf6711; rcuid=660724e65c20de8e73c16721; _ym_uid=1711744229317944692; _ym_d=1711744229; cancel_mobile_app=0; 4lapy_site_v7=current; testcookie=e0a5fe5fe86ada300005a1978e97b378493ad3f; tmr_lvid=7b30db167a8ac6ca57507dc556fb261e; tmr_lvidTS=1711744229852; _gid=GA1.2.298437446.1711744230; BX_USER_ID=c8e531ffd3ffb9bcdbf8521e978bdebd; _ymab_param=llkJgoz2a5COW6MLS0yE10VY2QsiHL-ES3FRmNQ_ZapQjz2Bka00FyHIT7YzyFERblwJEIy99TEFIGr4WapOGxf1CYE; _userGUID=0:lud4bh99:TpdmyHQqfTyY31TwgwjUcs75lfanu1Ka; _ym_isad=1; _gpVisits={"isFirstVisitDomain":true,"idContainer":"1000259C"}; __exponea_etc__=c4a7d40e-70e0-4078-b223-1560aff18d41; user_geo_location=%5B%5D; 4LP_product_subscribe=YEgE9enZ6H3BAB4WwT5eqSU4VMEuCFX1; show_mobile_app=null; hide_mobile_app=1; __exponea_time2__=1.272449254989624; skipCache=0; dSesn=c4508c3f-af99-a2fd-3a84-27b47d1d78f0; _dvs=0:ludskxkm:mhysvmIx9TA7iiFYUOII3QBmY~mSmSUd; _ga=GA1.2.356706601.1711744230; _ga_GRN90Z74D3=GS1.1.1711784979.2.1.1711785021.18.0.0; _ga_C98WC28BDH=GS1.2.1711784980.2.1.1711785022.18.0.0; _gp1000259C={"hits":15,"vc":1,"ac":1,"a6":1}; amp_932404=iwqtRtHYuT0GCGOxODpogU...1hq75bt7u.1hq75d6jb.0.0.0; digi_uc=W1siY3YiLCIxNTExNjEiLDE3MTE3ODUwMjQ1NzddLFsiY3YiLCIzMTA5MCIsMTcxMTc1MDA1NDQxMV0sWyJjdiIsIjE1NTY3OCIsMTcxMTc0NDgxNDM0OF1d; tmr_detect=0%7C1711785029800',
            'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjM0NTMzODkiLCJhcCI6IjMyODAxMDM4MyIsImlkIjoiNGFkNzFlMjU4MmY1ZGE3MCIsInRyIjoiODdmYTMxMzFjMjg5Y2IzZGJiYzMxOTc5MzNlZmEyYjAiLCJ0aSI6MTcxMTc4NTIwNjcyMH19',
            'referer': 'https://4lapy.ru/catalog/koshki/korm-koshki/sukhoy/?section_id=3&sort=popular&page=5',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'traceparent': '00-87fa3131c289cb3dbbc3197933efa2b0-4ad71e2582f5da70-01',
            'tracestate': '3453389@nr=0-1-3453389-328010383-4ad71e2582f5da70----1711785206720',
            'user-agent': f'{agent.random}',
            'x-requested-with': 'XMLHttpRequest',
        }

    def get_data(self):
        """Собираем информацию"""
        # Получаем список товаров со страницы

        for p in range(1, self.page + 1):
            print(f'Собираем данные со страницы: {p}')
            response = requests.get(
                f'https://4lapy.ru/catalog/koshki/korm-koshki/sukhoy/?section_id=3&sort=popular&page={p}').text

            soup = BeautifulSoup(response, 'lxml')

            # Сохраняем все id, чтобы в будущем пройти по ним
            productid = []
            data = soup.find_all(class_='b-common-item')
            for d in data:
                if d.get('data-productid') is not None:
                    productid.append(d.get('data-productid'))

            # В параметры помещаем наш список с id и указываем номер страницы
            params = {
                'section_id': '3',
                'sort': 'popular',
                'page': f'{self.page}',
                'product[]': productid,
            }

            # Отправляем запрос
            response_info = requests.get('https://4lapy.ru/ajax/catalog/product-info/', params=params,
                                         headers=self.headers).json()

            # Получаем список всех id продуктов, если честно уже запутался, столько тут этих id =)
            products = response_info.get('data').get('products')

            # Сохраняем все их в список
            save_products = []

            for p in products:
                idItems = products.get(p).get('offers')
                save_products.append(idItems)

            """
            И вот тут самое сложное для мозга, сначала получаем длину списка,
            потом проходимся по этой длине, далее по индексу открываем заходим в список и переходим по нужнному id 
            ( ВЗРЫВ МОЗГА )
            После декодируем строку в json формат, предварительно заменив одинарные кавычки на двойные, а то ломается.
            Получаем список продуктов и дальше забираем нужные значения
            """

            for i in range(0, len(save_products)):
                for t in save_products[i]:
                    dec = save_products[i].get(t).get('ecommerce').replace("'", '"')
                    start_index = dec.find("{")
                    end_index = dec.rfind("}") + 1
                    json_string = dec[start_index:end_index]

                    data = json.loads(json_string)

                    products = data['ecommerce']['click']['products']

                    id_ = products[0].get('id')
                    name = products[0].get('name')
                    price = products[0].get('price')
                    brand = products[0].get('brand')

                    result = {"id": id_, "name": name, "price": price, "brand": brand}
                    self.whrite_csv(result)

    @staticmethod
    def whrite_csv(result):
        with open("data_fourpaws.csv", mode="a", encoding='utf8') as w_file:
            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
            file_writer.writerow([result['id'], result['name'],
                                  result['price'], result['brand']])

if __name__ == '__main__':
    run = FourPawsParse()
    run.get_data()



