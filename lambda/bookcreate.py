import json
import boto3
import uuid

# Initialising the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('books')  # The name of your DynamoDB table

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        title = body['title']
        
        # Creating an Item with a unique id and with the passed title
        item = {
            'id': str(uuid.uuid4()),
            'title': title
        }
        
        # Inserting an item into the table
        table.put_item(Item=item)
        
        response = {
            'statusCode': 200
        }
        return response  # Returning a 200 if the item has been inserted
    except Exception as e:
        error_response = {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
        return error_response
