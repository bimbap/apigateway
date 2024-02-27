import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('books')

    try:
        id = event['pathParameters']['id']
        response = table.delete_item(
            Key={'id': id}
        )
        return {
            'statusCode': 200
        }
    except Exception as e:
        return {
            'statusCode': 500
        }
