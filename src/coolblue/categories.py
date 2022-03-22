import os
import json

import requests
from bs4 import BeautifulSoup


def get_categories():
    domain = "https://www.coolblue.de"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64;"
                      " rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;"
                  "q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    try:
        response = requests.get(url=domain, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        categories_tag = soup.find(class_="js-swipeable-content-wrapper")\
            .find_all(class_="card__title")
        for main_cat in categories_tag[:2]:
            main_category_name = main_cat.text.strip()
            main_category_url = main_cat.get('href')

            category_response = requests.get(
                url=f"{domain}{main_category_url}", headers=headers
            )
            print(category_response.status_code)
            soup = BeautifulSoup(category_response.text, "lxml")
            sub_categories_tag = soup.find(
                class_="js-swipeable-content-wrapper"
            ).find_all(class_="card__title")
            for sub_cat in sub_categories_tag[:2]:
                sub_category_name = sub_cat.text.strip()
                sub_category_url = sub_cat.get('href')
                if ".html" in sub_category_url:
                    continue
                url = f"{domain}{sub_category_url}/filter"
                list_response = requests.get(url, headers=headers)
                print(list_response.status_code)
                soup = BeautifulSoup(list_response.text, "lxml")

                product_list = soup.find_all(class_="product-card__title")
                for a in product_list[:2]:
                    link = f'{domain}{a.find(class_="link").get("href")}'
                    print(link)
                    response_detail = requests.get(link, headers=headers)
                    print(response_detail.status_code)
                    soup = BeautifulSoup(response_detail.text, "lxml")

                    product_name = soup.find("h1", class_="js-product-name").text.strip()

                    img_container = soup.find(class_="product-media-gallery__item")
                    image_url = img_container.find(
                        "img", class_="product-media-gallery__item-image"
                    ).get("src")

                    competitor = "coolblue"
                    competitor_detail = "coolblue.de"
                    sku = ""
                    brand = ""
                    product_specs = soup.find(class_="mb--6")\
                        .find(class_="product-specs")\
                        .find_all(class_="product-specs__list-item")
                    for sp in product_specs:
                        t = sp.find(class_="js-spec-title").text.strip()
                        if "rtikelnummer" in t:
                            sku = sp.find(class_="js-spec-value").text.strip()
                        if "Marke" in t:
                            brand = sp.find(class_="js-spec-value").text.strip()

                    base_price = soup.find(class_="sales-price__current")\
                        .text.strip().replace("-", "0")
                    saving_price = "0"
                    _saving_price = soup.find(class_="sales-price__former-price")
                    if _saving_price is not None:
                        saving_price = _saving_price.text.strip()

                    cart_btn = soup.find(class_="js-add-to-cart-button")
                    available_online = "N"
                    if cart_btn is not None:
                        available_online = "Y"

                    delivery_time = ""
                    delivery_cost = ""
                    deliver_str = soup.find(class_="icon-with-text")\
                        .find(class_="icon-with-text__text")
                    if deliver_str is not None:
                        deliver_str = deliver_str.text.strip().split(",")
                        _delivery_cost = deliver_str[1].split(" ")
                        delivery_time = deliver_str[0] + _delivery_cost[0].lower()
                        delivery_cost = _delivery_cost[2]

                    description = ""
                    if description is not None:
                        description = soup.find(
                            "div",
                            {"class": "cms-content hide@sm-down"}
                        ).find("p").text.strip()

                    breadcrumbs = soup.find("ol", class_="breadcrumbs").find_all(class_="breadcrumbs__item")[:-1]
                    categories = list()
                    for cname in breadcrumbs:
                        categories.append(cname.text.strip())

                    obj = {
                        "product_name": product_name,
                        "image_url": image_url,
                        "competitor": competitor,
                        "competitor_detail": competitor_detail,
                        "sku": sku,
                        "brand": brand,
                        "base_price": base_price,
                        "saving_price": saving_price,
                        "available_online": available_online,
                        "delivery_time": delivery_time,
                        "delivery_cost": delivery_cost,
                        "description": description,
                        "categories": categories,
                    }
                    with open("main.json", "w") as f:
                        json.dump(obj, f, indent=4, ensure_ascii=False)
                    exit()




                    # path = f"data/{main_category_name.replace(' ', '_').lower()}/" \
                    #        f"{sub_category_name.replace(' ', '_').lower()}"
                    # if not os.path.exists(path):
                    #     os.makedirs(path)
    except Exception as e:
        print(e)
