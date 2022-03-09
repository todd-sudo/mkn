import datetime
import json
import os

import requests

from src.config.settings import CATEGORIES_RIGLA


cookies = {
        "PHPSESSID": "b607f4b1f0346324759878139794b932",
        "popmechanic_sbjs_migrations": "popmechanic_1418474375998=1|||1471519752600=1|||1471519752605=1",
        "private_content_version": "6e7e5f46faf100cac593bcd7ef24025b",
        "quoteId": "2ea6a214c66c020f125aa3c669b00388",
        "regionSuggested": "1",
    }
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "X-APP": "WEB",
    "Accept": "*/*"
}


def parses_data(
        req_url: str,
        category_id: int,
        category_name: str,
        page: int,
):
    data = {
        "query": 'query categoryProducts($pageSize: Int!, '
                 '$currentPage: Int!) {\n    products: pro'
                 'ductsElastic(pageSize: $pageSize, sort: {is'
                 '_in_stock:DESC,search_weight:ASC,product_qty'
                 ':DESC}, currentPage: $currentPage, filter: '
                 f'{{category_id: {{eq: \"{category_id}\"}}}}, applyFilter: {{}}) '
                 '{\n        total_count\n        page_info {\n     '
                 '       page_size\n            current_page\n        }\n    '
                 '    filters {\n            request_var\n            additional_data\n            glossary_term {\n          '
                 '      title\n                url_key\n                description\n                short_description\n        '
                 '    }\n            name\n            filter_items_count\n            filter_items {\n             '
                 '   items_count\n                value_string\n                label\n            }\n        }\n     '
                 '   apply_filters {\n            attribute_label\n            request_var\n            value_label\n      '
                 '      value_string\n        }\n        items {\n            id\n            sku\n            name\n     '
                 '       rec_need\n            delivery\n            delivery_status\n            is_isg\n            is_x\n    '
                 '        price_isg\n            termolabil_preparat\n            thermolabile\n            url_key\n       '
                 '     promo_label\n            promo_label_ext {\n                name\n                color\n            '
                 '    url\n            }\n            orig_preparat {\n                label\n            }\n            thumbnail {\n  '
                 '              url\n                label\n            }\n            price {\n                oldPrice{\n    '
                 '                amount\n                    {\n                        value\n                    }\n         '
                 '       }\n                regularPrice {\n                    amount {\n                        value\n      '
                 '              }\n                }\n            }\n            manufacturer_id {\n                label\n    '
                 '        }\n            is_in_stock\n            is_isg\n            is_x\n            manufactures_url\n     '
                 '       brands_url\n            manufactures_url\n            categories{\n                id\n             '
                 '   name\n            }\n            emias_Id\n            unit_quantity\n            description_set_attributes {\n    '
                 '            attribute_label\n                values {\n                    value\n                  '
                 '  url_key\n                }\n                glossary_term {\n                    title\n            '
                 '        short_description\n                    description\n                    url_key\n           '
                 '     }\n            }\n        }\n    }\n}\n',
        "variables": {"pageSize": 100, "currentPage": page}
    }

    response = requests.post(
        f"{req_url}/graphql",
        json=data,
        cookies=cookies,
        headers=headers
    )

    data_json = response.json().get("data").get("products").get("items")
    if not data_json:
        return []
    products: list = list()
    for item in data_json:
        specs = list()
        specs_data = item.get("description_set_attributes")
        for s in specs_data:
            key = s.get("attribute_label")
            value = s.get("values")[0].get("value")
            specs.append({key: value})

        price = None
        if item.get("price").get("regularPrice") is not None:
            price = item.get("price").get("regularPrice").get("amount").get(
                "value")

        obj = {
            "код товара": item.get("sku"),
            "наименование": item.get("name"),
            "имя группы": category_name,
            "цена": price,
            "производитель": item.get("manufacturer_id").get("label"),
            "характеристики": specs,
        }
        products.append(obj)

    return products


def get_products_rigla():
    base_path = "data/rigla"
    with open(f"{base_path}/categories/categories.json", "r") as file:
        regions = json.load(file)

    for req_url in regions:
        reg_name = req_url.split("/")[2].split(".")[0]
        print(f"Регион: {reg_name}")

        root_path = f"{base_path}/parses_data_{datetime.datetime.now()}/{reg_name}".replace(" ", "_")
        if not os.path.exists(root_path):
            os.makedirs(root_path)

        products_category: list = []

        for category_id in CATEGORIES_RIGLA:
            category_name = CATEGORIES_RIGLA.get(category_id)
            print(f"Категория: {category_name}")

            for page in range(1000):
                if page == 0:
                    continue

                # возвращает список товаров с 1 страницы
                products_data = parses_data(
                    req_url=req_url,
                    category_id=category_id,
                    category_name=category_name,
                    page=page,
                )
                if not products_data:
                    print(f"Категория {category_name} закончилась. Товаров спаршено: {len(products_data)}")
                    break
                products_category += products_data
                print(f"Страница {page}")

            # save data to JSON files
            cat = category_name.replace(" ", "_").lower()
            with open(f"{root_path}/{cat}.json", "w") as file:
                json.dump(products_category, file, indent=2, ensure_ascii=False)


