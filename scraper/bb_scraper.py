"""
Please make sure to have chromedriver in your path.
This modeule is dependent on BestBuy and Wallmart changing their DOMs 
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os, re
from time import sleep
from logger import setup_custom_logger
from models import Bestbuy, Base, engine, db_session


log = setup_custom_logger(__file__)  # Initialize the logger for this module
bb_products = []
Base.metadata.create_all(bind=engine)  # Creates the tables in the DB if not existing


def best_buy_search(search_product):
    """
    Searches for the product passed as an search_product and returns the availability, url and prices of the product
    Finally stores it in the SQLlite DB
    """
    opts = Options()
    # opts.add_argument("--headless") # Comment out for debugging
    opts.add_argument(
        f"-user-agent={'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}"
    )
    try:
        driver = webdriver.Chrome(options=opts, service_log_path=os.devnull)
    except Exception as err:
        log.error(f"WebDriver creation errored out with: {err}")
        raise
    wait = WebDriverWait(driver, 20)
    driver.get("http://www.bestbuy.com")

    try:
        """
        Closes the landing banners on the bestbuy.com website to get to search box
        """
        element = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="widgets-view-email-modal-mount"]/div/div/div[1]/div/div/div/div/button',
                )
            )
        )
        element.click()
    except Exception as war:
        log.warning(f"No banner showed up on bestbuy.com landing page: {war}")

    try:
        """
        Enters the search string into the search bar of Best Buy website
        """
        element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#gh-search-input"))
        )
        sleep(2)
        element.send_keys(search_product)
        (
            wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "header-search-button"))
            )
        ).click()
    except Exception as err:
        log.error(f"Unable to click on the search bar and enter search word: {err}")
        driver.quit()
        raise

    try:
        """
        Stores all the results returned into items iterable
        """
        items = driver.find_elements_by_class_name("sku-item")
    except Exception as err:
        log.error(f"couldn't build the product items list: {err}")
        driver.quit()
        raise
    for item in items:
        try:
            """
            Determines id the product is available and collects all other info to store in the DB
            """
            product_status = item.find_element_by_class_name(
                "add-to-cart-button"
            ).get_attribute("innerText")
        except Exception as err:
            log.error(
                f"Product {search_product} status couldn't be determined as part of bestbuy scrape"
            )
        try:
            if product_status == "Add to Cart":
                sku_value = item.find_element_by_class_name("sku-header")
                product_url = (
                    "www.bestbuy.com"
                    + (re.findall(r'"(.*?)"', sku_value.get_attribute("innerHTML")))[0]
                )
                sku_unique = product_url.split("=")[-1]
                product_name = sku_value.get_attribute("innerText")
                product_price = item.find_element_by_class_name(
                    "priceView-hero-price.priceView-customer-price"
                ).get_attribute("innerText")
                product_data = [
                    str(sku_unique),
                    str(product_name),
                    str(product_status),
                    str(product_url),
                    str(product_price),
                ]
                product_coll = Bestbuy(*product_data)
                bb_products.append(product_coll)
        except Exception as inf:
            log.info(f"{search_product} parsing had issues: {inf}")
    try:
        db_session.bulk_save_objects(bb_products)
        db_session.commit()
    except Exception as err:
        log.error(f"Couldn't commit bestbuy result to DB: {err}")
        db_session.rollback()
        driver.quit()
        raise
    driver.quit()


"""
Sample execution:
This module is a piece of a larger project. 
Code below is used to run this module stand alone, if required
"""


def main():
    best_buy_search(
        search_product="Sony Bravia"
    )  # replace "Sony Bravia" with whatever product you want to search for


if __name__ == "__main__":
    main()
