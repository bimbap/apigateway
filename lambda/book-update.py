"""AWS Lambda handler for updating an existing book record by ID."""

import json
import os
import boto3
from botocore.exceptions import ClientError

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


def _parse_body(event):
    raw_body = event.get('body')
    if isinstance(raw_body, str):
        return json.loads(raw_body) if raw_body.strip() else {}
    return raw_body if isinstance(raw_body, dict) else {}


def lambda_handler(event, context):
    """Handle PUT /books/{id} requests."""
    try:
        print('Received event:', json.dumps(event))
        path_params = event.get('pathParameters') or {}
        book_id = path_params.get('id')

        if not book_id:
            return _build_response(400, {'error': 'Missing id in path parameters'})

        body = _parse_body(event)
        title = str(body.get('title', '')).strip()

        if not title:
            return _build_response(400, {'error': 'Missing title in request body'})

        response = table.update_item(
            Key={'id': book_id},
            UpdateExpression='SET title = :title',
            ConditionExpression='attribute_exists(id)',
            ExpressionAttributeValues={':title': title},
            ReturnValues='ALL_NEW'
        )

        return _build_response(200, {
            'message': f'Book with id {book_id} updated successfully',
            'item': response.get('Attributes', {'id': book_id, 'title': title})
        })
    except ClientError as exc:
        if exc.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return _build_response(404, {'error': f'Book with id {book_id} not found'})
        print('DynamoDB error updating book:', str(exc))
        return _build_response(500, {'error': str(exc)})
    except json.JSONDecodeError:
        return _build_response(400, {'error': 'Invalid JSON payload'})
    except Exception as exc:
        print('Error updating book:', str(exc))
        return _build_response(500, {'error': str(exc)})
