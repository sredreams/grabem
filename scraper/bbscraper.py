from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By
import os
import re
from time import sleep

# Need to add input string validation here for search word


def best_buy_search(search_word):
    """
    Searches for the product passed as an search word and prints the status and prices.
    """
    opts = Options()
    # opts.add_argument("--headless") # Commented out for debugging

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
    for (
        item
    ) in items:  # the print will be replaced with return once done with debugging.
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
                print(
                    "Price--",
                    (
                        item.find_element_by_class_name(
                            "priceView-hero-price.priceView-customer-price"
                        ).get_attribute("innerText")
                    ),
                )
        except:
            print("properties not found")
        print("\n\n")
    driver.quit()


def walmart_search(search_word):
    """
    Crawls through the wallmart website looking for the search_word
    which is the product name in this case. This function is not fully functional yet.
    """
    opts = Options()
    # opts.add_argument("--headless") # Commented out for debugging
    opts.add_argument(
        f"-user-agent={'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}"
    )
    driver = webdriver.Chrome(options=opts, service_log_path=os.devnull)
    wait = WebDriverWait(driver, 20)
    driver.get("https://www.walmart.com")
    element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#global-search-input"))
    )
    element.send_keys(search_word)
    (wait.until(EC.element_to_be_clickable((By.ID, "global-search-submit")))).click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "arrange-fill")))
    items = driver.find_elements_by_class_name("arrange-fill")
    for item in items:  # not-iterable returns bunch of child divs
        try:
            print(
                item.find_element_by_xpath(
                    '//*[@id="searchProductResult"]/div/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/a'
                )
            )
        except:
            print("properties not found")
