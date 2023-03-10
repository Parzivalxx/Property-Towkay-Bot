import json
from unittest import main, TestCase

uri = 'https://www.propertyguru.com.sg/'


class TestWebscraperLambda(TestCase):
    def test_webscraper_success_listing_first(self):
        from src.lambda_function import create_url

        event_data = 'tests/test_events/success_listing_first.json'
        with open(event_data, 'r') as f:
            event = json.load(f)

        url = create_url(uri, event)
        with open('tests/test_events/success_string.txt', 'r') as f:
            success_string = f.read()

        self.assertEqual(url, success_string)

    def test_webscraper_success_listing_not_first(self):
        from src.lambda_function import create_url

        event_data = 'tests/test_events/success_listing_not_first.json'
        with open(event_data, 'r') as f:
            event = json.load(f)

        url = create_url(uri, event)
        with open('tests/test_events/success_string.txt', 'r') as f:
            success_string = f.read()

        self.assertEqual(url, success_string)

    def test_create_preference_failure(self):
        from src.lambda_function import create_url

        event_data = 'tests/test_events/failure_listing_absent.json'
        with open(event_data, 'r') as f:
            event = json.load(f)

        url = create_url(uri, event)

        self.assertEqual(url, '')


if __name__ == '__main__':
    main()
