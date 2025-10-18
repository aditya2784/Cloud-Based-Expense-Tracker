import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('DDB_TABLE', 'ExpenseTracker')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body') or '{}')
        user_id = body['UserID']
        expense_id = body['ExpenseID']
        table.delete_item(Key={'UserID': user_id, 'ExpenseID': expense_id})
        return {'statusCode': 200, 'body': json.dumps({'message': 'Expense deleted'})}
    except Exception as e:
        return {'statusCode': 400, 'body': json.dumps({'error': str(e)})}
