from time import sleep
import json

from selenium import webdriver
from selenium.common.exceptions import InvalidCookieDomainException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
options.add_argument(f"User-Agent={user_agent}")

with open('olx_cookies.json', 'r') as f:
    cookies = json.load(f)

driver = webdriver.Chrome(options=options)

driver.get("https://www.olx.ua/account/")

for cookie in cookies:
    if cookie['domain'] == 'ua.login.olx.com':
        cookie['sameSite'] = 'None'
        driver.add_cookie(cookie)

driver.refresh()

wait = WebDriverWait(driver, 10)

#send_message_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'css-xwy0pu')))
#send_message_button.click()

sleep(100)
html_content = driver.page_source

with open('index.html', 'w') as f:
    f.write(html_content)

driver.quit()
