import os
import csv
import uuid

import requests

from .utils import format_categories


def get_products():
    """ Собирает товары по всем категориям
    """
    path_csv = "data/product/csv"
    if not os.path.exists(path_csv):
        os.makedirs(path_csv)
    categories = format_categories()

    for category_dict in categories:
        products = list()
        all_props: list = []
        for category_name in category_dict:
            page = 1
            for p in range(1, 1000):
                data = {
                    "csrf_token": "128f87dbafae4e490acc98bf6f56e8e6",
                    "page": str(page),
                    "pageSize": "500",
                    "sortColumn": "popularity",
                    "sortDirection": "desc",
                }
                url = f"https://tvoydom.ru/api/internal/catalog/{category_dict.get(category_name)}"

                response = requests.post(url=url, data=data)
                cards = response.json().get("cards")
                if not cards:
                    print("Нет товаров. Exit!!!")
                    break

                for c in cards:
                    props = c.get("props")
                    name = c.get("name")
                    vendor = ""
                    if "(" in name:
                        vendor = name.split("(")[1].replace(")", "")
                    obj = {
                        "артикул": vendor,
                        "кол-во": c.get("overallStock") or 0,
                        "код товара": c.get("code"),
                        "наименование": name,
                        "имя группы": category_name,
                        "цена": c.get("price"),
                        "актуальная цена": c.get("actualPrice"),
                        "цена со скидкой": c.get("discountPrice") or 0,
                        "скидка": c.get("discount") or 0,
                        "сумма бонуса": c.get("bonusAmount"),
                        "id бренда": c.get("brandId"),
                        "название бренда": c.get("brand"),
                    }
                    obj.update(props)

                    products.append(obj)

                    for prop in props:
                        all_props.append(prop)
                print(f"Страница {page} | Категория {category_name}")
                page += 1

            path_csv = "data/tvoidom/product/csv"
            if not os.path.exists(path_csv):
                os.makedirs(path_csv)

            all_props_new = set(all_props)
            fields = [
                "артикул",
                "кол-во",
                "код товара",
                "наименование",
                "имя группы",
                "цена",
                "актуальная цена",
                "цена со скидкой",
                "скидка",
                "сумма бонуса",
                "id бренда",
                "название бренда",
            ] + list(all_props_new)

            with open(f"{path_csv}/data_{category_name.lower().replace(' ', '_')}.csv", "w") as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                writer.writerows(products)
                print(f"CSV ЗАПИСАН!!!")





