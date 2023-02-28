import json
from dynamo import get_dynamo_table


def lambda_handler(event, context):
    print(event)

    user_id = event['pathParameters']['user_id']

    try:
        user_details = get_dynamo_table().get_item(Key={"user_id": user_id})
        print(user_details)

        return {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps("Preference retrieved successfully"),
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 404,
            "headers": {},
            "body": "Not Found",
        }
