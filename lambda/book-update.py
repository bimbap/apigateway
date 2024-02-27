import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('books')

    try:
        body = json.loads(event['body'])
        id = event['pathParameters']['id']
        title = body['title']
        
        response = table.put_item(
            Item={
                'id': id,
                'title': title
            }
        )
        return {
            'statusCode': 200
        }
    except Exception as e:
        return {
            'statusCode': 500
        }
