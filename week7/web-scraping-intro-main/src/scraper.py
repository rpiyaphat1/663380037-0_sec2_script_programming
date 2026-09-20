# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

class WikipediaScraper:
    """Class for scraping article titles and headings from Wikipedia"""
    
    def __init__(self, target_url):
        self.target_url = target_url

    def _get_html_content(self):
        """Downloads HTML from target URL"""
        print(f"Downloading data from: {self.target_url}")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(self.target_url, headers=headers, timeout=10)
            response.raise_for_status()
            print("Successfully downloaded content.")
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def scrape_article_data(self):
        """Scrapes article title and subheadings"""
        html_content = self._get_html_content()
        if not html_content:
            return None

        soup = BeautifulSoup(html_content, 'html.parser')

        title_tag = soup.find('h1', id='firstHeading')
        article_title = title_tag.get_text(strip=True) if title_tag else "Title Not Found"

        headings = []
        for heading in soup.find_all(['h2', 'h3']):
            text = heading.get_text(strip=True)
            if text and not any(text.startswith(ignore) for ignore in ['Contents', 'Navigation', 'Personal tools', 'Search']):
                headings.append(text)

        return {
            "title": article_title,
            "headings": headings
        }