from time import sleep
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


with open('olx_cookies.json', 'r') as f:
    cookies = json.load(f)

driver = webdriver.Chrome()

for cookie in cookies:
    if cookie['domain'] == 'ua.login.olx.com':
        print(cookie['domain'])
        cookie['sameSite'] = "Lax"
        driver.add_cookie(cookie)

driver.get('https://ua.login.olx.com/')

for cookie in cookies:
    if cookie['domain'] != 'ua.login.olx.com':
        print(cookie['domain'])
        cookie['sameSite'] = "Lax"
        driver.add_cookie(cookie)

wait = WebDriverWait(driver, 10)

#send_message_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'css-xwy0pu')))
#send_message_button.click()

sleep(100)

html_content = driver.page_source

with open('index.html', 'w') as f:
    f.write(html_content)

driver.quit()
