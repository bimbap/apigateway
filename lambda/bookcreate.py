"""AWS Lambda handler for creating a new book record in DynamoDB."""

import json
import os
import uuid
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


def _parse_body(event):
    raw_body = event['body']
    if isinstance(raw_body, str):
        return json.loads(raw_body) if raw_body.strip() else {}
    return raw_body if isinstance(raw_body, dict) else {}


def lambda_handler(event, context):
    """Handle POST /books requests via Lambda Proxy Integration."""
    try:
        print('Received event:', json.dumps(event))
        body = _parse_body(event)
        title = str(body.get('title', '')).strip()

        if not title:
            return _build_response(400, {'error': "Field 'title' is required"})

        item = {
            'id': str(uuid.uuid4()),
            'title': title
        }
        table.put_item(Item=item)

        return _build_response(201, {
            'message': 'Item created successfully',
            'id': item['id'],
            'item': item
        })
    except json.JSONDecodeError:
        return _build_response(400, {'error': 'Invalid JSON payload'})
    except Exception as exc:
        print('Error creating book:', str(exc))
        return _build_response(500, {'error': str(exc)})
