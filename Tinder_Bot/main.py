from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

facebook_username = "your email"
facebook_password = "your password"

# setup the chrome browser and make sure its in English
service = Service("your chrome driver path")
options = Options()
options.add_argument("--lang=en")
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

driver.get("https://tinder.com/app/recs")

wait = WebDriverWait(driver, 10)
# clicks accept on the cookies
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="o-1556761323"]/div/div[2]/div/div/div[1]/button/span'))).click()

# clicks on the login button
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="o-1556761323"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/span'))).click()

# clicks on the login to facebook popup button
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="o-1335420887"]/div/div/div[1]/div/div[3]/span/div[2]/button/span[2]'))).click()

# wait for the login page to pop
wait.until(EC.new_window_is_opened(driver.window_handles))
driver.switch_to.window(driver.window_handles[-1])

insert_email = driver.find_element(By.XPATH, '//*[@id="email"]')
insert_email.send_keys(facebook_username)

insert_password = driver.find_element(By.XPATH, '//*[@id="pass"]')
insert_password.send_keys(facebook_password, Keys.ENTER)

# waits until the facebook login is closed and switch back to the tinder page
wait.until(EC.number_of_windows_to_be(1))
driver.switch_to.window(driver.window_handles[0])

# clicks on allow location
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="o-1335420887"]/div/div/div/div/div[3]/button[1]/span'))).click()

# clicks on enable notifications
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="o-1335420887"]/div/div/div/div/div[3]/button[2]/span'))).click()

# checks if the see who likes u button appears and if so press "maybe later"
if wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="o-1335420887"]/div/div/div/div[3]/button[2]/span'))):
    driver.find_element(By.XPATH, '//*[@id="o-1335420887"]/div/div/div/div[3]/button[2]/span').click()

sleep(2)
    
# swipe until u r out of likes
have_likes = True
while have_likes:
    try:
        # checks if u r out of likes
        if WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="o-1335420887"]/div/div/div[3]/button[2]'))):
            driver.find_element(By.XPATH, '//*[@id="o-1335420887"]/div/div/div[3]/button[2]').click()
            have_likes = False
        else:
            continue
        # add tinder to home screen reject
        WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="o-1335420887"]/div/div/div[2]/button[2]/span'))).click()

        # if there is a match will press ok and will continue to swipe (idk if it works cause i didn't got a match)
        if WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.itsAMatch a'))):
            driver.find_element(By.CSS_SELECTOR, '.itsAMatch a').click()
    except TimeoutException:
        pass

    # clicks on the like button
    actions = ActionChains(driver)
    actions.send_keys(Keys.ARROW_RIGHT)
    actions.perform()


driver.quit()

