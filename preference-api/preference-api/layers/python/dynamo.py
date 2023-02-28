import os
import boto3


def get_dynamo_table():
    table_name = os.environ.get('TABLE', 'Preferences')
    region = os.environ.get('REGION', 'ap-southeast-1')
    aws_environment = os.environ.get('AWSENV', 'AWS_SAM_LOCAL')

    if aws_environment == 'AWS_SAM_LOCAL':
        preferences_table = boto3.resource('dynamodb', endpoint_url="http://dynamodb:8000")
    else:
        preferences_table = boto3.resource('dynamodb', region_name=region)

    return preferences_table.Table(table_name)
