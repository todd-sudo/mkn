import json
import os
import time

from src.services.selenium import get_web_driver_options


def get_categories():
    driver = get_web_driver_options()
    domain = "https://rigla.ru/"
    path = "data/rigla/categories/"
    if not os.path.exists(path):
        os.makedirs(path)

    try:
        cities = list()
        driver.get(domain)

        time.sleep(3)
        print("load page")
        panel = driver.find_element_by_class_name("header__upper-container")
        time.sleep(1)
        _ = panel.find_element_by_class_name("navigation__city-item").click()
        time.sleep(1)
        regions = driver.find_elements_by_class_name("region-selector__region")
        i = 0
        for r in regions:
            if i < 2:
                i += 1
                continue

            r.click()
            cit = driver.find_element_by_class_name("region-selector__city")
            url = cit.get_attribute("href")
            cities.append(f"https://{url.split('/')[2]}")

        with open(f"{path}/categories.json", "w") as file:
            json.dump(cities, file, indent=4, ensure_ascii=False)

    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()



