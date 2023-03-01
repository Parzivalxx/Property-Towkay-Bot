import json
from unittest import main, TestCase, mock
import os
import sys

import boto3
from moto import mock_dynamodb


@mock.patch.dict(
    os.environ, {'TABLE': 'Mock_Preferences',
                 'REGION': 'ap-southeast-1',
                 'AWSENV': 'MOCK'}
)
@mock_dynamodb
class TestCreatePreference(TestCase):
    def setUp(self) -> None:
        sys.path.append(os.getcwd() + '/layers/python')
        self.dynamodb = boto3.client('dynamodb', region_name='ap-southeast-1')
        self.dynamodb.create_table(
            TableName="Mock_Preferences",
            KeySchema=[
                {"AttributeName": "user_id", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "user_id", "AttributeType": "S"}
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )

    def tearDown(self) -> None:
        self.dynamodb.delete_table(TableName="Mock_Preferences")
        sys.path.remove(os.getcwd() + '/layers/python')

    def test_create_preference_success(self):
        from src.create_preference import app

        event_data = 'tests/test_events/create_preference.json'
        with open(event_data, 'r') as f:
            event = json.load(f)

        response = app.lambda_handler(event, '')
        body = json.loads(response['body'])

        self.assertEqual(response['statusCode'], 201)
        self.assertEqual(body['user_id'], 'lol3')
        self.assertEqual(body['district'], 'nice')
        self.assertEqual(body['property_type'], 'good')
        self.assertEqual(body['min_price'], 1)
        self.assertEqual(body['max_price'], 2)
        self.assertEqual(body['bedrooms'], 3)
        self.assertEqual(body['min_floor_size'], 4)
        self.assertEqual(body['max_floor_size'], 5)
        self.assertEqual(body['tenure'], '999')
        self.assertEqual(body['min_build_year'], 6)
        self.assertEqual(body['max_build_year'], 7)
        self.assertEqual(body['floor_level'], 'high')

    def test_create_preference_failure(self):
        from src.create_preference import app

        event_data = 'tests/test_events/create_preference.json'
        with open(event_data, 'r') as f:
            event = json.load(f)
        event['body'] = ''

        response = app.lambda_handler(event, '')

        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(response['body'], 'Bad request')


if __name__ == '__main__':
    main()
