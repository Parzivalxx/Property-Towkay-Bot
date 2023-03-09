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
class TestDeletePreference(TestCase):
    def setUp(self) -> None:
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

    def test_delete_preference_success(self):
        from src.delete_preference import app

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

        event_data = 'tests/test_events/delete_preference.json'
        with open(event_data, 'r') as f:
            event = json.load(f)

        response = app.lambda_handler(event, '')

        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], 'Preference deleted successfully')

    def test_delete_action_failure(self):
        from src.delete_preference import app

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

        event_data = 'tests/test_events/delete_preference.json'
        with open(event_data, 'r') as f:
            event = json.load(f)

        response = app.lambda_handler(event, '')

        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(response['body'], 'Bad Request')


if __name__ == '__main__':
    main()
