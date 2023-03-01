import json
from dynamo import get_dynamo_table
from typing import Dict, Union


def lambda_handler(event, context):
    print(event)

    if not event['body']:
        return {"statusCode": 400,
                "headers": {},
                "body": "Bad Request"}

    preference: Dict[str, Union[int, str]] = json.loads(event["body"])

    search_params = {
        "user_id": event['pathParameters']['user_id']
    }

    try:
        db_response = get_dynamo_table().update_item(
            Key=search_params,
            UpdateExpression="""
            set district=:d, \
            property_type=:p, \
            min_price=:minp, \
            max_price=:maxp, \
            bedrooms=:b, \
            min_floor_size=:minf, \
            max_floor_size=:maxf, \
            tenure=:t, \
            min_build_year=:minb, \
            max_build_year=:maxb, \
            floor_level=:f, \
            """,
            ExpressionAttributeValues={
                ":d": preference['district'],
                ":p": preference['property_type'],
                ":minp": preference['min_price'],
                ":maxp": preference['max_price'],
                ":b": preference['bedrooms'],
                ":minf": preference['min_floor_size'],
                ":maxf": preference['max_floor_size'],
                ":t": preference['tenure'],
                ":minb": preference['min_build_year'],
                ":maxb": preference['max_build_year'],
                ":f": preference['floor_level'],
            },
            ConditionExpression="attribute_exists(user_id)",
            ReturnValues="ALL_NEW"
        )
        print(db_response)

        return {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps(db_response['Attributes']),
        }

    except Exception as e:
        print(e)
        return {"statusCode": 400,
                "headers": {},
                "body": "Bad Request"}
