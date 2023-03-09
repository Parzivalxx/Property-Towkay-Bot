import json
from dynamo import get_dynamo_table
from typing import Dict, Union
from decimal import Decimal


def lambda_handler(event, context):
    print(event)

    if not event['body']:
        return {"statusCode": 400,
                "headers": {},
                "body": "Bad Request"}

    try:
        preference: Dict[str, Union[int, str]] = json.loads(event["body"])
        search_params = {
            "user_id": int(event['pathParameters']['user_id'])
        }
        db_response = get_dynamo_table().update_item(
            Key=search_params,
            UpdateExpression=(
                "set listing_type=:l, "
                "property_type=:pt, "
                "property_type_code=:ptc, "
                "min_price=:minp, "
                "max_price=:maxp, "
                "min_floor_size=:minf, "
                "max_floor_size=:maxf, "
                "min_build_year=:minb, "
                "max_build_year=:maxb, "
                "bedrooms=:b, "
                "floor_level=:f, "
                "tenure=:t, "
                "district=:d, "
                "job_frequency_hours=:j"
            ),
            ExpressionAttributeValues={
                ":l": preference['listing_type'],
                ":pt": preference['property_type'],
                ":ptc": preference['property_type_code'],
                ":minp": Decimal(str(preference['min_price'])),
                ":maxp": Decimal(str(preference['max_price'])),
                ":minf": Decimal(str(preference['min_floor_size'])),
                ":maxf": Decimal(str(preference['max_floor_size'])),
                ":minb": Decimal(str(preference['min_build_year'])),
                ":maxb": Decimal(str(preference['max_build_year'])),
                ":b": preference['bedrooms'],
                ":f": preference['floor_level'],
                ":t": preference['tenure'],
                ":d": preference['district'],
                ":j": preference['job_frequency_hours'],
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


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
