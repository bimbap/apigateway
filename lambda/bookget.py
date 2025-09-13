import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('books')

def lambda_handler(event, context):
    try:
        response = table.scan()
        data = response.get('Items', [])

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            'body': json.dumps(data)
        }
    except Exception as e:
        # log error supaya ketahuan di CloudWatch
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Internal Server Error'})
        }
