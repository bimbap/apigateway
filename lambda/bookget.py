"""AWS Lambda handler for listing all book records from DynamoDB."""

import json
import os
import boto3

TABLE_NAME = os.environ.get('TABLE_NAME', 'books')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

CORS_HEADERS = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Requested-With',
    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
}


def lambda_handler(event, context):
    """Handle GET /books requests and return all stored items."""
    try:
        response = table.scan()
        items = response.get('Items', [])

        # Handle DynamoDB pagination if table exceeds 1 MB scan limit
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items', []))

        return {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': json.dumps(items)
        }
    except Exception as exc:
        print('Error scanning books:', str(exc))
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'error': 'Internal Server Error'})
        }
