import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('books')

def lambda_handler(event, context):
    id = event['pathParameters']['id']
    try:
        response = table.get_item(
            Key={
                'id': id
            }
        )
        item = response['Item']
        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500
        }
