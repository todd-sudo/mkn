import csv
import time

import requests
from bs4 import BeautifulSoup

from src.coolblue.db import get_cursor_db
from src.coolblue.utils import get_categories


def get_products():
    domain = "https://www.coolblue.de"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64;"
                      " rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;"
                  "q=0.9,image/avif,image/webp,*/*;q=0.8"
    }

    response = requests.get(url=domain, headers=headers)
    print(response.status_code)
    soup = BeautifulSoup(response.text, "lxml")
    categories_tag = soup.find(class_="js-swipeable-content-wrapper")
    if categories_tag is not None:
        categories_tag = categories_tag.find_all(class_="card__title")

    for main_cat in categories_tag:
        try:
            main_category_name = main_cat.text.strip()
            main_category_url = main_cat.get('href')
            print(f"Парсинг main категории - {main_category_name}")
            category_response = requests.get(
                url=f"{domain}{main_category_url}", headers=headers
            )
            print(category_response.status_code)
            soup = BeautifulSoup(category_response.text, "lxml")
            sub_categories_tag = soup.find(
                class_="js-swipeable-content-wrapper"
            )
            if sub_categories_tag is not None:
                sub_categories_tag = sub_categories_tag.find_all(class_="card__title")
            for sub_cat in sub_categories_tag:
                try:
                    sub_category_name = sub_cat.text.strip()
                    print(f"Парсинг sub категории - {sub_category_name}")
                    sub_category_url = sub_cat.get('href')
                    if ".html" in sub_category_url:
                        continue
                except Exception as e:
                    print(e)
                    time.sleep(5)
                    continue
                
                u = f"{domain}{sub_category_url}/filter"
                r = requests.get(url=u, headers=headers)
                soup = BeautifulSoup(r.text, "lxml")
                page_count = int(soup.find_all(class_="pagination__item")[-2].text.strip())
                print(f"Страниц всего - {page_count}")
                for page in range(page_count+1):
                    try:
                        if page == 0:
                            continue

                        print(f"Страница - {page}")
                        url = f"{domain}{sub_category_url}/filter?seite={page}"
                        print(f"CATEGORY URL = {url}")
                        list_response = requests.get(url, headers=headers)
                        print(list_response.status_code)
                        soup = BeautifulSoup(list_response.text, "lxml")

                        product_list = soup.find_all(class_="product-card__title")
                        if product_list is None:
                            print("вышел с цикла с страницами")
                            break

                        cur, con = get_cursor_db()
                        products = []
                        for a in product_list:
                            try:
                                link = f'{domain}{a.find(class_="link").get("href")}'
                                print(link)
                                response_detail = requests.get(link, headers=headers)
                                soup = BeautifulSoup(response_detail.text, "lxml")
                                product_name = ""
                                _product_name = soup.find("h1", class_="js-product-name")
                                if _product_name is not None:
                                    product_name = _product_name.text.strip()
                                image_url = ""
                                img_container = soup.find(class_="product-media-gallery__item")
                                if img_container is not None:
                                    image_url = img_container.find(
                                        "img", class_="product-media-gallery__item-image"
                                    )
                                    if image_url is not None:
                                        image_url = image_url.get("src")

                                competitor = "coolblue"
                                competitor_detail = "coolblue.de"
                                sku = ""
                                brand = ""
                                product_specs = soup.find(class_="mb--6")
                                if product_specs is not None:
                                    product_specs = product_specs.find(class_="product-specs")
                                    if product_specs is not None:
                                        product_specs = product_specs.find_all(
                                            class_="product-specs__list-item"
                                        )

                                for sp in product_specs:
                                    t = sp.find(class_="js-spec-title").text.strip()
                                    if "rtikelnummer" in t:
                                        sku = sp.find(class_="js-spec-value").text.strip()
                                    if "Marke" in t:
                                        brand = sp.find(class_="js-spec-value").text.strip()

                                base_price = ""
                                _base_price = soup.find(class_="sales-price__current")
                                if _base_price is not None:
                                    base_price = _base_price.text.strip().replace("-", "0")
                                saving_price = "0"
                                _saving_price = soup.find(class_="sales-price__former-price")
                                if _saving_price is not None:
                                    saving_price = _saving_price.text.strip().replace("-", "0")

                                cart_btn = soup.find(class_="js-add-to-cart-button")
                                available_online = "N"
                                if cart_btn is not None:
                                    available_online = "Y"

                                delivery_time = ""
                                delivery_cost = ""
                                deliver_str = soup.find(class_="icon-with-text")
                                if deliver_str is not None:
                                    deliver_str = deliver_str.find(class_="icon-with-text__text")
                                if deliver_str is not None:
                                    deliver_str = deliver_str.text.strip().split(",")
                                    _delivery_cost = deliver_str[1].split(" ")
                                    delivery_time = deliver_str[0] + _delivery_cost[0].lower()
                                    delivery_cost = _delivery_cost[2]

                                description = ""
                                _description = soup.find(
                                    "div",
                                    {"class": "cms-content hide@sm-down"}
                                )
                                if _description is not None:
                                    description = _description.find("p")
                                    if description is not None:
                                        description = description.text.strip()

                                _categories = []

                                breadcrumbs = soup.find("ol", class_="breadcrumbs").find_all(class_="breadcrumbs__item")[:-1]

                                if breadcrumbs is not None:
                                    for cname in breadcrumbs:
                                        _categories.append(cname.text.strip())

                                c1, c2, c3, c4, c5 = get_categories(_categories)
                                obj = (
                                    competitor,
                                    competitor_detail,
                                    sku,
                                    product_name,
                                    c1,
                                    c2,
                                    c3,
                                    c4,
                                    c5,
                                    saving_price,
                                    base_price,
                                    available_online,
                                    delivery_time,
                                    delivery_cost,
                                    brand,
                                    link,
                                    image_url,
                                    description
                                )
                                products.append(obj)

                            except Exception as e:
                                print(e)
                                time.sleep(5)
                                continue
                        print(products)
                        query = """
                        insert into product values (
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                            ?, ?, ?, ?, ?, ?, ?, ?
                            )
                        """
                        cur.executemany(query, products)
                        con.commit()
                        print(f"Сохранено {len(products)} товаров")
                        con.close()

                    except Exception as e:
                        print(e)
                        time.sleep(5)
                        continue

        except Exception as e:
            print(e)
            time.sleep(10)
            continue

    # con.close()
    # fields = [
    #     "Competitor",
    #     "Competitor Detail",
    #     "SKU",
    #     "Name",
    #
    #     "Category1",
    #     "Category2",
    #     "Category3",
    #     "Category4",
    #     "Category5",
    #
    #     "Price Saving",
    #     "Price Base",
    #     "Available Online",
    #     "Delivery Time",
    #     "Delivery Cost",
    #     "Brand",
    #     "Url",
    #     "Image url",
    #     "Description",
    # ]
    # with open("main.csv", "w") as file:
    #     writer = csv.DictWriter(file, fieldnames=fields)
    #     writer.writeheader()
    #     writer.writerows(products)
    #     print(f"CSV ЗАПИСАН!!!")


def run_parser_coolblue():
    get_products()


