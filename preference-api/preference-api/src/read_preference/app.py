import json
from decimal import Decimal
from dynamo import get_dynamo_table


def lambda_handler(event, context):
    print(event)

    try:
        user_id = int(event['pathParameters']['user_id'])
        user_details = get_dynamo_table().get_item(Key={"user_id": user_id})
        print(user_details)

        return {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps(user_details['Item'], cls=DecimalEncoder)
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 404,
            "headers": {},
            "body": "Not Found",
        }


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
