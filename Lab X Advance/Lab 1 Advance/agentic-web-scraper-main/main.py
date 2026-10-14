# -*- coding: utf-8 -*-
# agentic-web-scraper/main.py
import sys
import os
import logging
import json

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config_parser import ConfigParser
from scraper_agent import ScraperAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    config_file_path = os.path.join(os.path.dirname(__file__), 'configs', 'example_site_config.json')
    try:
        config_parser = ConfigParser(config_file_path)
        config = config_parser.load_config()
        scraper_agent = ScraperAgent(config, browser='chrome', headless=True)
        scraper_agent.run()
        print(f"\nScraped {len(scraper_agent.scraped_products)} products:")
        print(json.dumps(scraper_agent.scraped_products, indent=4, ensure_ascii=False))
    except Exception as e:
        logging.critical(f"Execution failed: {e}")

if __name__ == "__main__":
    main()