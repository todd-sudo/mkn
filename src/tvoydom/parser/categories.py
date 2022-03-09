import json
import os
import time

from src.services.selenium import get_web_driver_options


def get_categories():
    """Собирает категории"""
    driver = get_web_driver_options()
    try:
        domain = "https://tvoydom.ru/"
        driver.get(domain)
        print("Перешел на страницу")
        driver.find_element_by_class_name("popmechanic-close").click()
        time.sleep(1)
        print("Закрыл рекламу")
        btn = driver.find_element_by_class_name("js-catalog-dropdown-btn")
        btn.click()
        links = driver.find_elements_by_class_name("catalog-menu__link")
        urls = []
        for link in links:
            urls.append({link.text.strip(): link.get_attribute("href")})

        print(urls)

        path = "data/tvoidom/categories/tvoydom"
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f"{path}categories.json", "w") as file:
            json.dump(urls, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()


