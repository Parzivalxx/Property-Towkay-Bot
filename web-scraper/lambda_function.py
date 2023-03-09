import json
import os
from project_config import (
    URI,
    preference_mapper,
    query_mapper
)
from WebScraper import WebScraper
from typing import Dict


def lambda_handler(event, context):
    try:
        print('Starting application...')
        SCRAPING_ANT_TOKEN = os.environ['SCRAPING_ANT_TOKEN']
        url = create_url(
            url=URI,
            event=event
        )
        print('base url: ' + url)
        web_scraper = WebScraper(
            url=url,
            frequency_hours=event['job_frequency_hours'],
            token=SCRAPING_ANT_TOKEN
        )
        links = web_scraper.scrape_pages()
        print(links)
        return {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps(links)
        }

    except Exception as e:
        print(e)

    return {
        "statusCode": 500,
        "headers": {},
        "body": "Internal Server Error"
    }


def create_url(url: str, event: Dict) -> str:
    for key, value in event.items():
        if key in ['user_id', 'job_frequency_hours']:
            continue
        mapped_key = query_mapper.get(key, key)
        if mapped_key == 'listing_type':
            value = preference_mapper[key][value]
            url += f'property-for-{value}?market=residential&{mapped_key}={value}'
            continue
        if mapped_key == 'property_type_code[]':
            property_type = event['property_type']
            value = preference_mapper[key][property_type][value]
            if isinstance(value, list):
                for item in value:
                    url += f'&{mapped_key}={item}'
            else:
                url += f'&{mapped_key}={value}'
            continue
        if isinstance(value, int):
            url += f'&{mapped_key}={value}'
        else:
            if key not in preference_mapper:
                url += f'&{mapped_key}={value}'
                continue
            value = preference_mapper[key][value]
            url += f'&{mapped_key}={value}'
    url += '&search=true'
    return url
