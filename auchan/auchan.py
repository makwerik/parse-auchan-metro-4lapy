import csv

import requests
from fake_useragent import UserAgent


class AuchanParse:
    """Парсим мясо птицы. Магазин - Ашан"""

    def __init__(self, page=4):
        """Инициализируем headers, куки убрал, можно добавить рандомных юзер-агентов"""
        agent = UserAgent()

        self.headers = {
            'User-Agent': f'{agent.random}',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json;charset=utf-8',
            'Origin': 'https://www.auchan.ru',
            'Connection': 'keep-alive',
            'Referer': 'https://www.auchan.ru/catalog/ptica-myaso/ptica/?page=2',
            # 'Cookie': 'qrator_jsr=1711733377.798.HG3DX6xdhVuMtOcA-0v4ribtst79e63nk54fulkag9vk6t0rq-00; qrator_jsid=1711733377.798.HG3DX6xdhVuMtOcA-ase22j2kjg7e2jffqbdtms039h97kq9c; haveChat=true; region_id=1; merchant_ID_=1; methodDelivery_=2; _GASHOP=001_Mitishchi; rrpvid=414031474029631; _userGUID=0:lucxuxku:_5ZfBj8PtUzUTf5sClPK8aXk~5x~bCV8; dSesn=7317f8f9-0a4b-8962-627f-352a307a676b; _dvs=0:lucxuxku:tU~6xfTXRLET4xSeuvCP5U1VEB8HRd2d; rcuid=6606fa855e0cb646695c69e1; tmr_lvid=2872cb51481e06d1a2e79299febf81d9; tmr_lvidTS=1711733382133; tmr_detect=1%7C1711733419610; qrator_jsr=1711733377.798.HG3DX6xdhVuMtOcA-0v4ribtst79e63nk54fulkag9vk6t0rq-00; qrator_jsr=1711733377.798.HG3DX6xdhVuMtOcA-0v4ribtst79e63nk54fulkag9vk6t0rq-00; _ymab_param=cu-ReNUxnQCAM3yyiBUP4x9hh-hBDEs2wxwIcLZWti4orpSH6DQQWlZ4rya5KG-jfKvLlRUR1QHRrzQ_H0BiFMKh9mY; _ym_uid=1711733382515575799; _ym_d=1711733382; mindboxDeviceUUID=69ba32c0-f3ef-4197-bd2d-406a19ff4410; directCrm-session=%7B%22deviceGuid%22%3A%2269ba32c0-f3ef-4197-bd2d-406a19ff4410%22%7D; _ym_isad=1; _ym_visorc=w; digi_uc=W10=; _clck=1fw2c9x%7C2%7Cfkh%7C0%7C1549; _clsk=gnrasa%7C1711733409834%7C2%7C1%7Ci.clarity.ms%2Fcollect; acceptCookies_=true',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
        self.json_data = {
            'filter': {
                'category': 'ptica',
                'promo_only': False,
                'active_only': False,
                'cashback_only': False,
            },
        }
        self.page = page

    def get_data(self):
        print("Собираю данные")
        """Собираем данные, как указано в тз"""
        for p in range(1, self.page + 1):
            params = {
                'merchantId': '1',
                'page': f'{p}',
                'perPage': '40',
            }

            response = requests.post(
                'https://www.auchan.ru/v1/catalog/products',
                params=params,
                headers=self.headers,
                json=self.json_data,
            )

            items = response.json().get('items')

            for i in items:
                productId = i.get('productId')
                name = i.get('title')
                link = f'https://www.auchan.ru/product/{i.get("code")}/'
                regular_price = i.get('price').get('value')
                try:
                    old_price = i.get('oldPrice').get('value')
                except AttributeError:
                    old_price = ''
                brand = i.get('brand').get("name")
                data = {"productId": productId, "name": name,
                        "link": link, "regular_price": regular_price,
                        "old_price": old_price, "brand": brand}
                self.whrite_csv(data)

    @staticmethod
    def whrite_csv(data):
        with open("data_auchan.csv", mode="a", encoding='utf8') as w_file:
            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
            file_writer.writerow([data['productId'], data['name'],
                                  data['link'], data['regular_price'],
                                  data['old_price'], data['brand']])


if __name__ == '__main__':
    a = AuchanParse()
    a.get_data()
