import os
import json


def format_categories() -> list:
    path = "data/categories/tvoydom"
    with open(f"{path}categories.json", "r") as file:
        urls_file = json.load(file)

    urls = list()
    for urls_dict in urls_file:
        for name, url in urls_dict.items():
            urls.append({name: url.split("/")[4]})
    return urls
