from dynamo import get_dynamo_table


def lambda_handler(event, context):
    print(event)

    user_id: str = event['pathParameters']['user_id']

    try:
        db_response = get_dynamo_table().delete_item(
            Key={"user_id": user_id},
            ConditionExpression="attribute_exists(user_id)",
        )
        print(db_response)

        return {
            "statusCode": 200,
            "body": "Preference deleted successfully",
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 400,
            "body": "Bad Request",
        }
