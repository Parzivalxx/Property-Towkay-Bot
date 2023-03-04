import json
import sys
from unittest import main, TestCase, mock
import os

import boto3
from moto import mock_dynamodb


@mock.patch.dict(
    os.environ, {'TABLE': 'Mock_Preferences',
                 'REGION': 'ap-southeast-1',
                 'AWSENV': 'MOCK'}
)
@mock_dynamodb
class TestUpdatePreference(TestCase):
    def setUp(self):
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
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1}
        )

    def tearDown(self) -> None:
        self.dynamodb.delete_table(TableName='Mock_Preferences')
        sys.path.remove(os.getcwd() + '/layers/python')

    def test_update_preference_success(self):
        from src.update_preference import app
        mock_item = {
            "user_id": {"S": "mock"},
            "district": {"S": "mock1"},
            "property_type": {"S": "mock2"},
            "min_price": {"N": "10"},
            "max_price": {"N": "11"},
            "bedrooms": {"N": "12"},
            "min_floor_size": {"N": "13"},
            "max_floor_size": {"N": "14"},
            "tenure": {"S": "freehold"},
            "min_build_year": {"N": "15"},
            "max_build_year": {"N": "16"},
            "floor_level": {"S": "low"}
        }
        self.dynamodb.put_item(TableName='Mock_Preferences', Item=mock_item)

        event_data = 'tests/test_events/update_preference.json'
        with open(event_data, 'r') as f:
            event = json.load(f)

        response = app.lambda_handler(event, '')
        body = json.loads(response['body'])

        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(body['user_id'], 'mock')
        self.assertEqual(body['district'], 'nice')
        self.assertEqual(body['property_type'], 'good')
        self.assertEqual(body['min_price'], '1')
        self.assertEqual(body['max_price'], '2')
        self.assertEqual(body['bedrooms'], '3')
        self.assertEqual(body['min_floor_size'], '4')
        self.assertEqual(body['max_floor_size'], '5')
        self.assertEqual(body['tenure'], '999')
        self.assertEqual(body['min_build_year'], '6')
        self.assertEqual(body['max_build_year'], '7')
        self.assertEqual(body['floor_level'], 'high')

    def test_update_preference_failure(self):
        from src.update_preference import app

        mock_item = {
            "user_id": {"S": "fake"},
            "district": {"S": "mock1"},
            "property_type": {"S": "mock2"},
            "min_price": {"N": "10"},
            "max_price": {"N": "11"},
            "bedrooms": {"N": "12"},
            "min_floor_size": {"N": "13"},
            "max_floor_size": {"N": "14"},
            "tenure": {"S": "freehold"},
            "min_build_year": {"N": "15"},
            "max_build_year": {"N": "16"},
            "floor_level": {"S": "low"}
        }
        self.dynamodb.put_item(TableName='Mock_Preferences', Item=mock_item)

        event_data = 'tests/test_events/update_preference.json'
        with open(event_data, 'r') as f:
            event = json.load(f)

        response = app.lambda_handler(event, '')

        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(response['body'], 'Bad Request')


if __name__ == '__main__':
    main()
