from seleniumwire import webdriver

from src.config.settings import HEADLESS_MODE, PAUSE


def get_web_driver_options(proxy: dict = None) -> any:
    """Возвращает опции веб драйвера"""
    options = webdriver.FirefoxOptions()
    options.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    )
    options.set_preference("dom.webdriver.enabled", False)
    options.headless = HEADLESS_MODE

    profile = webdriver.FirefoxProfile()
    profile.set_preference('dom.webdriver.enabled', False)
    driver = webdriver.Firefox(
        executable_path="src/webdriver/geckodriver",
        options=options,
        # seleniumwire_options=proxy,
        firefox_profile=profile
    )
    driver.set_page_load_timeout(3600 * PAUSE * 2)
    return driver
