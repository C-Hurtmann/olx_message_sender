from time import sleep
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OLXParser:
    start_url = 'https://www.olx.ua/account/'
    root_url = 'https://www.olx.ua/'
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.driver.get(self.start_url)
        sleep(3)

    def tear_down(self):
        self.driver.quit()

    def add_cookies(self, cookies):
        for cookie in cookies:
            if cookie['domain'] == 'ua.login.olx.com':
                cookie['sameSite'] = 'None'
                self.driver.add_cookie(cookie)
        self.driver.refresh()

    def add_cookies_from_file(self, file):
        with open(file, 'r') as f:
            cookies = json.load(f)
        
        self.add_cookies(cookies)

    def gather_n_urls_from_main_page(self, n):
        self.driver.get(self.root_url)
        elements = self.driver.find_elements(By.XPATH, '//div[@class="mheight tcenter"]//a')
        self.gathered_urls = [elem.get_attribute("href") for elem in elements[:n]]
    
    def send_message_to_seller(self, url, message):
        self.driver.get(url)
        
        call_message_field_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-cy="ad-contact-message-button"]'))
            )
        call_message_field_button.click()

        message_field = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//textarea[@name="message.text"]'))
            )
        message_field.send_keys(message)

        submit_message_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Submit message"]'))
            )
        submit_message_button.click()

    def send_message_to_gathered_sellers(self, message):
        for url in self.gathered_urls:
            self.send_message_to_seller(url, message)

    def save_gathered_urls(self, file):
        with open(file, 'w') as f:
            for url in self.gathered_urls:       
                f.write(url + '\n')


if __name__ == '__main__':
    options = webdriver.ChromeOptions()

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    options.add_argument(f"User-Agent={user_agent}")
    
    driver = webdriver.Chrome(options=options)
    
    parser = OLXParser(driver)
    parser.add_cookies_from_file('cookies.json')
    parser.gather_n_urls_from_main_page(10)
    parser.save_gathered_urls('urls.txt')
    parser.send_message_to_gathered_sellers()
    parser.tear_down()