from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import time

class BrowserTools:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.cache = {}

    def search_google(self, query, num_results=3):
        search_url = f"https://www.google.com/search?q={query}"
        self.driver.get(search_url)
        search_results = self.driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf > a")
        top_urls = [result.get_attribute("href") for result in search_results[:num_results]]
        return top_urls

    def scrape_page(self, url, timeout=10):
        if url in self.cache:
            return self.cache[url]

        try:
            response = requests.get(url, timeout=timeout)
            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.title.string if soup.title else ""
            paragraphs = [p.get_text() for p in soup.find_all("p")]
            content = " ".join(paragraphs)

            self.cache[url] = {
                "url": url,
                "title": title,
                "content": content
            }

            return self.cache[url]
        except requests.exceptions.RequestException as e:
            print(f"Error scraping page: {url}")
            print(f"Error message: {str(e)}")
            return None

    def click_button(self, button_selector, timeout=10):
        try:
            button = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
            )
            button.click()
        except TimeoutException:
            print(f"Button not found or not clickable: {button_selector}")

    def fill_form(self, form_selector, data, timeout=10):
        try:
            form = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, form_selector))
            )
            for field, value in data.items():
                input_field = form.find_element(By.NAME, field)
                input_field.clear()
                input_field.send_keys(value)
            submit_button = form.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
        except TimeoutException:
            print(f"Form not found: {form_selector}")

    def find_element(self, selector, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element
        except TimeoutException:
            print(f"Element not found: {selector}")
            return None

    def extract_text(self, selector, timeout=10):
        element = self.find_element(selector, timeout)
        if element:
            return element.text
        return ""

    def close(self):
        self.driver.quit()

    def restart(self):
        self.close()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)