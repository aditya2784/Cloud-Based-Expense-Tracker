import json
import boto3
import uuid
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('DDB_TABLE', 'ExpenseTracker')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        data = json.loads(event.get('body') or '{}')
        user_id = data['UserID']
        expense_id = str(uuid.uuid4())
        item = {
            'UserID': user_id,
            'ExpenseID': expense_id,
            'Category': data.get('Category', 'General'),
            'Amount': float(data.get('Amount', 0)),
            'Date': data.get('Date', datetime.utcnow().date().isoformat()),
            'Description': data.get('Description', ''),
            'CreatedAt': datetime.utcnow().isoformat()
        }
        table.put_item(Item=item)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Expense added', 'ExpenseID': expense_id})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
