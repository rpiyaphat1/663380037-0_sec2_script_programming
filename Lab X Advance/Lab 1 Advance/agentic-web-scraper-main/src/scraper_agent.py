# -*- coding: utf-8 -*-
# agentic-web-scraper/src/scraper_agent.py
import time
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from driver_manager import DriverManager
from data_models import Product
from utils import wait_for_element, robust_click, save_data_to_json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ScraperAgent:
    """Agentic web scraper driven by JSON rules."""
    
    def __init__(self, config, browser='chrome', headless=True):
        self.config = config
        self.driver_manager = DriverManager(browser_name=browser, headless=headless)
        self.driver = None
        self.scraped_products = []
        self.max_pages = config.get("max_pages", 3)

    def _get_element_text(self, parent_element, selector):
        try:
            return parent_element.find_element(By.CSS_SELECTOR, selector).text.strip()
        except NoSuchElementException:
            return None

    def _get_element_attribute(self, parent_element, selector, attribute):
        try:
            return parent_element.find_element(By.CSS_SELECTOR, selector).get_attribute(attribute).strip()
        except NoSuchElementException:
            return None

    def _parse_product_data(self, item_element):
        selectors = self.config["item_data_selectors"]
        name = self._get_element_text(item_element, selectors.get("name", ""))
        price = self._get_element_text(item_element, selectors.get("price", ""))
        description = self._get_element_text(item_element, selectors.get("description", "")) if selectors.get("description") else None
        url = self._get_element_attribute(item_element, selectors.get("url", ""), "href") if selectors.get("url") else None
        image_url = self._get_element_attribute(item_element, selectors.get("image_url", ""), "src") if selectors.get("image_url") else None

        if name and price:
            return Product(name=name, price=price, description=description, url=url, image_url=image_url)
        return None

    def scrape_page(self):
        item_elements = self.driver.find_elements(By.CSS_SELECTOR, self.config["item_container_selector"])
        logging.info(f"Found {len(item_elements)} item containers on page.")
        for item_element in item_elements:
            product = self._parse_product_data(item_element)
            if product:
                self.scraped_products.append(product.to_dict())

    def run(self):
        self.driver = self.driver_manager.get_driver()
        if not self.driver:
            return

        try:
            self.driver.get(self.config["start_url"])
            current_page = 1
            while current_page <= self.max_pages:
                logging.info(f"Scraping page {current_page}...")
                self.scrape_page()
                time.sleep(self.config.get("delay_between_pages", 2))

                pagination_selector = self.config.get("pagination_selector")
                if pagination_selector and current_page < self.max_pages:
                    if robust_click(self.driver, By.CSS_SELECTOR, pagination_selector):
                        current_page += 1
                    else:
                        break
                else:
                    break
        finally:
            self.driver_manager.quit_driver()
            save_data_to_json(self.scraped_products, "scraped_products.json")