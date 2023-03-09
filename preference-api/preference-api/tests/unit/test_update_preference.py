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
                {"AttributeName": "user_id", "AttributeType": "N"}
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1}
        )

    def tearDown(self) -> None:
        self.dynamodb.delete_table(TableName='Mock_Preferences')
        sys.path.remove(os.getcwd() + '/layers/python')

    def test_update_preference_success(self):
        from src.update_preference import app
        mock_item = {
            "user_id": {"N": "1"},
            "listing_type": {"S": "Sale"},
            "property_type": {"S": "HDB"},
            "property_type_code": {"S": "5 room"},
            "min_price": {"N": "700000"},
            "max_price": {"N": "800000"},
            "min_floor_size": {"N": "1000"},
            "max_floor_size": {"N": "1400"},
            "min_build_year": {"N": "1980"},
            "max_build_year": {"N": "2010"},
            "bedrooms": {"S": "3"},
            "floor_level": {"S": "High"},
            "tenure": {"S": "99-year"},
            "district": {"S": "D19"},
            "job_frequency_hours": {"N": "3"}
        }
        self.dynamodb.put_item(TableName='Mock_Preferences', Item=mock_item)

        event_data = 'tests/test_events/update_preference.json'
        with open(event_data, 'r') as f:
            event = json.load(f)

        response = app.lambda_handler(event, '')
        body = json.loads(response['body'])

        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(body['user_id'], '1')
        self.assertEqual(body['listing_type'], 'Rent')
        self.assertEqual(body['property_type'], 'Condo')
        self.assertEqual(body['property_type_code'], '5 room')
        self.assertEqual(body['min_price'], '700000')
        self.assertEqual(body['max_price'], '800000')
        self.assertEqual(body['min_floor_size'], '1000')
        self.assertEqual(body['max_floor_size'], '1400')
        self.assertEqual(body['min_build_year'], '2000')
        self.assertEqual(body['max_build_year'], '2010')
        self.assertEqual(body['bedrooms'], '4')
        self.assertEqual(body['floor_level'], 'High')
        self.assertEqual(body['tenure'], '99-year')
        self.assertEqual(body['district'], 'D20')
        self.assertEqual(body['job_frequency_hours'], '1')

    def test_update_preference_failure(self):
        from src.update_preference import app

        mock_item = {
            "user_id": {"N": "2"},
            "listing_type": {"S": "Sale"},
            "property_type": {"S": "HDB"},
            "property_type_code": {"S": "5 room"},
            "min_price": {"N": "700000"},
            "max_price": {"N": "800000"},
            "min_floor_size": {"N": "1000"},
            "max_floor_size": {"N": "1400"},
            "min_build_year": {"N": "1980"},
            "max_build_year": {"N": "2010"},
            "bedrooms": {"S": "3"},
            "floor_level": {"S": "High"},
            "tenure": {"S": "99-year"},
            "district": {"S": "D19"},
            "job_frequency_hours": {"N": "3"}
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
