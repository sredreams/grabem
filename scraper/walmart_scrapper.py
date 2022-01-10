"""
Work in progress
Walmart scrapper to look for products
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os, re
from logger import setup_custom_logger

log = setup_custom_logger(__file__)


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
            walmart_product = item.find_element_by_xpath(
                '//*[@id="searchProductResult"]/div/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/a'
            )
            return walmart_product
        except Exception as err:
            log.error(f"Walmart scrapper errored out with error: {err}")
    driver.quit()
