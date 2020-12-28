from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from util import ProductData, construct_url_for_product, clean_stock_string

WEB_TIMEOUT = 30
TOTAL_RETRIES = 2

def build_web_driver(driver_location: str):
    option = webdriver.ChromeOptions()
    option.add_argument('— incognito')
    option.headless = True
    option.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(executable_path=driver_location, chrome_options=option)
    driver.set_page_load_timeout(WEB_TIMEOUT)
    return driver

class MicrocenterBuddy:

    def __init__(self, chrome_driver_location: str) -> None:
        self.chrome_driver = build_web_driver(chrome_driver_location)

    def total_product_count(self, product_info: ProductData) -> int:
       try:
           return self._retrieve_product_count_string(product_info)
       except Exception as e:
           print(f"Something happened -> {e}")
           return 0

    def _retrieve_product_count_string(self, product_info: ProductData, retry_count: int = 0) -> str:
        
        product_url = construct_url_for_product(product_info)

        if retry_count >= TOTAL_RETRIES:
            print(f"Have already attempting to reach page {product_url} {TOTAL_RETRIES} times. Will not try again")
            raise Exception(f"Failed to find product count for page -> {product_url}")

        
        print(f"Attempt {retry_count + 1}: Trying to pull proudct info from {product_url}")

        target_class = 'inventoryCnt'
        try:
            self.chrome_driver.get(product_url)

            element: WebElement = self.chrome_driver.find_element_by_class_name(target_class)
            
            stripped_text : str = clean_stock_string(str(element.text))

            if stripped_text == 'sold out':
                return 0
            else:
                return int(stripped_text)

        except TimeoutException as te:
            
            print(f"Got a timeout exception after waiting for {30} seconds")

            #   Let's try things again
            self._reload_driver()
            return self._retrieve_product_count_string(product_info, retry_count + 1)

        except NoSuchElementException as e:
            print(f"Failed to find element of type {target_class} with exception -> {e}")
        
        return 0

    def _reload_driver(self):

        if self.chrome_driver is not None:
            self.chrome_driver.quit()

        self.chrome_driver = build_web_driver()

