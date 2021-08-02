from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import fake_useragent
import os
import re
import argparse
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--product", help="Product Name")
args = parser.parse_args()


def best_buy_search(search_word):
    useragent = fake_useragent.UserAgent()
    opts = Options()
    # opts.add_argument("--headless")

    opts.add_argument(
        f"-user-agent={'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}"
    )
    driver = webdriver.Chrome(options=opts, service_log_path=os.devnull)
    wait = WebDriverWait(driver, 20)
    driver.get("http://www.bestbuy.com")

    element = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="widgets-view-email-modal-mount"]/div/div/div[1]/div/div/div/div/button',
            )
        )
    )
    element.click()

    element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#gh-search-input"))
    )
    sleep(2)
    element.send_keys(search_word)
    (
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "header-search-button")))
    ).click()
    product_list = driver.find_element_by_class_name("sku-item-list")
    items = product_list.find_elements_by_class_name("sku-item")
    for item in items:
        try:
            print(
                "Product Status--",
                (
                    item.find_element_by_class_name("add-to-cart-button").get_attribute(
                        "innerText"
                    )
                ),
            )
        except:
            print("not found")
        try:
            if (
                item.find_element_by_xpath(
                    "//*[contains(@id, 'add-to-cart-button')]"
                ).get_attribute("innerText")
            ) == "Add to Cart":
                sku_value = item.find_element_by_class_name("sku-header")
                print(
                    "siteurl--",
                    "www.bestbuy.com"
                    + (re.findall(r'"(.*?)"', sku_value.get_attribute("innerHTML")))[0],
                )
                print("Product Name--", sku_value.get_attribute("innerText"))
        except:
            print("properties not found")
        print("\n\n")
    driver.quit()


best_buy_search(search_word=args.product)
