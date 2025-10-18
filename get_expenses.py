import json
import boto3
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('DDB_TABLE', 'ExpenseTracker')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        user_id = None
        # Support query string param or JSON body
        if event.get('queryStringParameters'):
            user_id = event['queryStringParameters'].get('UserID')
        if not user_id:
            body = json.loads(event.get('body') or '{}')
            user_id = body.get('UserID')
        if not user_id:
            raise ValueError("UserID is required")
        resp = table.query(
            KeyConditionExpression=Key('UserID').eq(user_id)
        )
        items = resp.get('Items', [])
        return {
            'statusCode': 200,
            'body': json.dumps({'expenses': items})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
