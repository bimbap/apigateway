"""AWS Lambda handler for retrieving a single book record by ID."""

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


def _build_response(status_code, payload):
    return {
        'statusCode': status_code,
        'headers': CORS_HEADERS,
        'body': json.dumps(payload)
    }


def lambda_handler(event, context):
    """Handle GET /books/{id} requests."""
    try:
        print('Received event:', json.dumps(event))
        path_params = event.get('pathParameters') or {}
        book_id = path_params.get('id')

        if not book_id:
            return _build_response(400, {'error': 'Missing id in path parameters'})

        response = table.get_item(Key={'id': book_id})
        item = response.get('Item')

        if not item:
            return _build_response(404, {'message': 'Item not found'})

        return _build_response(200, item)
    except Exception as exc:
        print('Error getting book:', str(exc))
        return _build_response(500, {'error': str(exc)})
