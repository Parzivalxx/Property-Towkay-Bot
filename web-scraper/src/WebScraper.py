import time
from scrapingant_client import ScrapingAntClient
from typing import List, Tuple
from bs4 import BeautifulSoup
from src.project_config import (
    MAX_PAGES,
    SCRAPER_INIT_RETRIES,
    SCRAPER_ERROR_RETRIES
)


class WebScraper:
    def __init__(self, url: str,
                 frequency_hours: int,
                 token: str):
        self.url = url
        self.token = token
        self.frequency_hours = frequency_hours
        self.soup = self.create_soup(self.url)

    def create_soup(self, url: str):
        found = False
        for i in range(SCRAPER_ERROR_RETRIES):
            print(f'Initialize scraper loop {i}...')
            try:
                for j in range(SCRAPER_INIT_RETRIES):
                    client = ScrapingAntClient(token=self.token)
                    result = client.general_request(url)
                    soup = BeautifulSoup(result.content, 'html.parser')
                    if 'captcha' in soup.text:
                        print(f'Retrying {j} / {SCRAPER_INIT_RETRIES}')
                        time.sleep(0.1)
                        if j > 0 and j % 10 == 0:
                            print('Connection reset, retrying in 30 secs...',
                                  flush=True)
                            time.sleep(30)
                        continue
                    if 'No Results' in soup.text:
                        print(f'Invalid URL, skipping {url}')
                    found = True
                    break
                if found:
                    return soup
            except Exception as e:
                print(e)
                print('Connection reset, retrying in 1 min...', flush=True)
                time.sleep(60)
        return

    def get_number_of_pages(self) -> int:
        if not self.soup:
            return 0
        pagination = self.soup.find('ul', class_='pagination')
        pages = 0
        try:
            if pagination.find_all('li', class_='pagination-next disabled'):
                pages = int(pagination.find_all('a')[0]['data-page'])
            else:
                pages = int(pagination.find_all('a')[-2]['data-page'])
        except AttributeError:
            cls = self.soup.find('h1', class_='title search-title')
            if cls and cls.text.split(' ')[2] == '0':
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
                continue
            if listing_recency[-1] == 'h':
                hours_ago = listing_recency[:-1]
                if int(hours_ago) < self.frequency_hours:
                    links.append((prop['title'], prop['href']))
        return links

    def scrape_pages(self) -> List[Tuple[str, str]]:
        pages = self.get_number_of_pages()
        print(f'Found {pages} pages')
        if pages == 0:
            return []
        pages = min(pages, MAX_PAGES)
        print(f'Scraping {pages} pages...')
        links = []
        links += self.get_links(self.soup)
        print(f'Page 1 / {pages} done')
        for page in range(2, pages + 1):
            if page == 2:
                question_idx = self.url.find('?')
                url = self.url[:question_idx] + '/2' + \
                    self.url[question_idx:]
            else:
                previous = f'/{page - 1}'
                url = f'/{page}'.join(url.split(previous))
            print(f'Page {page}: {url}')
            soup = self.create_soup(url)
            links += self.get_links(soup)
            print(f'Page {page} / {pages} done')
        return links
