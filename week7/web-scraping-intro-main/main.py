# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scraper import WikipediaScraper

def main():
    target_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    
    scraper = WikipediaScraper(target_url)
    scraped_data = scraper.scrape_article_data()

    if scraped_data:
        print("\n--- Wikipedia Scraping Result ---")
        print(f"Article Title: {scraped_data['title']}\n")
        print("Headings:")
        if scraped_data['headings']:
            for i, heading in enumerate(scraped_data['headings'][:15], 1):
                print(f"{i}. {heading}")
        else:
            print("No headings found.")
        print("---------------------------------")
    else:
        print("Failed to scrape data.")

if __name__ == "__main__":
    main()