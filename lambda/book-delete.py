"""AWS Lambda handler for deleting a book record by ID."""

import json
import os
import boto3

TABLE_NAME = os.environ['TABLE_NAME']
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
    """Handle DELETE /books/{id} requests."""
    try:
        print('Received event:', json.dumps(event))
        path_params = event.get('pathParameters') or {}
        book_id = path_params.get('id')

        if not book_id:
            return _build_response(400, {'error': 'Missing id in path parameters'})

        response = table.delete_item(
            Key={'id': book_id},
            ReturnValues='ALL_OLD'
        )

        if 'Attributes' in response:
            return _build_response(200, {'message': f'Book with id {book_id} deleted successfully'})

        return _build_response(404, {'error': f'Book with id {book_id} not found'})
    except Exception as exc:
        print('Error deleting book:', str(exc))
        return _build_response(500, {'error': str(exc)})
