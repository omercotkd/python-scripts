from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def check_if_can_buy_products():
    price_check = driver.find_elements(By.CSS_SELECTOR, '.product')
    for produce in price_check[::-1]:
        if produce.get_attribute('class') == 'product unlocked enabled':
            produce.click()


service = Service("C:\\Users\\omerc\\chromedriver_win32\\chromedriver.exe")
options = Options()
options.add_argument("--lang=en")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://orteil.dashnet.org/cookieclicker/")
clicker = driver.find_element(By.ID, "bigCookie")
buy_time = time.time() + 5
timeout = time.time() + 60 * 10

while True:
    clicker.click()
    if buy_time <= time.time():
        check_if_can_buy_products()
        buy_time = time.time() + 5
    if timeout <= time.time():
        break

driver.quit()










