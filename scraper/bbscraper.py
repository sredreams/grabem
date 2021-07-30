from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import fake_useragent
import os
from time import sleep


useragent = fake_useragent.UserAgent()
opts = Options()
opts.add_argument(f"-user-agent={useragent.random}")
# profile = webdriver.FirefoxProfile()
# profile.set_preference("general.useragent.override", useragent.random)
# profile.set_preference("dom.popup_maximum", 0)
# profile.set_preference("webdriver.load.strategy", "unstable")
# print(useragent.random)
# # options.add_argument("-devtools")

# driver = webdriver.Firefox(firefox_options=options, firefox_profile=profile)
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
sleep(5)
element.send_keys("PS5 Console")
(
    driver.find_element_by_xpath(
        "/html/body/div[2]/div/div/div[1]/header/div[1]/div/div[1]/div/form/button[2]"
    )
).click()

sleep(30)
driver.close()
driver.quit()
