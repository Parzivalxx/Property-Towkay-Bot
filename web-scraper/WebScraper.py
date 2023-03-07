import cloudscraper
import time
from typing import List, Tuple
from bs4 import BeautifulSoup
from project_config import (
    URI,
    SCRAPER_INIT_RETRIES,
    SCRAPER_ERROR_RETRIES
)


class WebScraper:
    def __init__(self, filters: str, frequency_hours: int):
        self.url = URI + filters
        self.soup = self.initialize_scraper(self.url)
        self.frequency_hours = frequency_hours

    def initialize_scraper(self, url: str):
        for i in range(SCRAPER_ERROR_RETRIES):
            print(f'Inititialize scraper loop {i}...')
            try:
                for j in range(SCRAPER_INIT_RETRIES):
                    scraper = cloudscraper.create_scraper(debug=True)
                    soup = BeautifulSoup(scraper.get(url).content, 'html-parser')
                    if 'captcha' in soup.text:
                        print(f'Retrying {j} / 50')
                        time.sleep(0.1)
                        if j % 10 == 0:
                            print('Connection reset, retrying in 30 secs...',
                                  flush=True)
                            time.sleep(30)
                        continue
                    if 'No Results' in soup.text:
                        print(f'Invalid URL, skipping {url}')
                    break
                return soup
            except Exception as e:
                print(e)
                print('Connection reset, retring in 1 min...', flush=True)
                time.sleep(60)

    def get_number_of_pages(self) -> int:
        pagination = self.soup.find('ul', class_='pagination')
        pages = 0
        try:
            if pagination.find_all('li', class_='pagination-next disabled'):
                pages = int(pagination.find_all('a')[0]['data-page'])
            else:
                pages = int(pagination.find_all('a')[-2]['data-page'])
        except AttributeError:
            cls = self.soup.find('h1', class_='title search-title')
            if cls.text.split(' ')[2] == '0':
                print('No property found. Scraping stopped.')
        return pages

    def get_links(self, soup) -> List[Tuple[str, str]]:
        links = []
        units = soup.find_all('div', itemtype='https://schema.org/Place')
        for unit in units:
            listing_recency = unit.find('div', class_='listing-recency').text
            prop = unit.find('a', class_='nav-link')
            if listing_recency[-1] == 'm':
                links.append((prop['title'], prop['href']))
            elif listing_recency[-1] == 'h':
                # early breaking for frequency 1 hour
                if self.frequency_hours == 1:
                    return links
                hours_ago = listing_recency[:-1]
                if int(hours_ago) < self.frequency_hours:
                    links.append((prop['title'], prop['href']))
        return links

    def scrape_pages(self, pages: int) -> List[Tuple[str, str]]:
        links = []
        links += self.get_links(self.soup)
        print(f'Page 1 / {pages} done')
        # for page in range(2, pages + 1):
        #     url = f'{URI}'
        #     soup = self.initialize_scraper()
