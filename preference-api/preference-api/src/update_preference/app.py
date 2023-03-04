import json
from dynamo import get_dynamo_table
from typing import Dict, Union
from decimal import Decimal
from src.update_preference.DecimalEncoder import DecimalEncoder


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
            UpdateExpression=(
                "set district=:d, "
                "property_type=:p, "
                "min_price=:minp, "
                "max_price=:maxp, "
                "bedrooms=:b, "
                "min_floor_size=:minf, "
                "max_floor_size=:maxf, "
                "tenure=:t, "
                "min_build_year=:minb, "
                "max_build_year=:maxb, "
                "floor_level=:f"
            ),
            ExpressionAttributeValues={
                ":d": preference['district'],
                ":p": preference['property_type'],
                ":minp": Decimal(str(preference['min_price'])),
                ":maxp": Decimal(str(preference['max_price'])),
                ":b": Decimal(str(preference['bedrooms'])),
                ":minf": Decimal(str(preference['min_floor_size'])),
                ":maxf": Decimal(str(preference['max_floor_size'])),
                ":t": preference['tenure'],
                ":minb": Decimal(str(preference['min_build_year'])),
                ":maxb": Decimal(str(preference['max_build_year'])),
                ":f": preference['floor_level']
            },
            ConditionExpression="attribute_exists(user_id)",
            ReturnValues="ALL_NEW"
        )
        print(db_response)

        return {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps(db_response['Attributes'], cls=DecimalEncoder)
        }

    except Exception as e:
        print(e)
        return {"statusCode": 400,
                "headers": {},
                "body": "Bad Request"}
