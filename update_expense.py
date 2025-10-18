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
        update_expr_parts = []
        expr_attr_vals = {}
        expr_attr_names = {}
        if 'Category' in body:
            update_expr_parts.append('Category = :c')
            expr_attr_vals[':c'] = body['Category']
        if 'Amount' in body:
            update_expr_parts.append('Amount = :a')
            expr_attr_vals[':a'] = float(body['Amount'])
        if 'Date' in body:
            update_expr_parts.append('#D = :d')
            expr_attr_vals[':d'] = body['Date']
            expr_attr_names['#D'] = 'Date'
        if 'Description' in body:
            update_expr_parts.append('Description = :desc')
            expr_attr_vals[':desc'] = body['Description']
        if not update_expr_parts:
            raise ValueError("No updatable fields provided")
        update_expression = 'SET ' + ', '.join(update_expr_parts)
        table.update_item(
            Key={'UserID': user_id, 'ExpenseID': expense_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expr_attr_vals,
            ExpressionAttributeNames=expr_attr_names or {},
            ReturnValues='ALL_NEW'
        )
        return {'statusCode': 200, 'body': json.dumps({'message': 'Expense updated'})}
    except Exception as e:
        return {'statusCode': 400, 'body': json.dumps({'error': str(e)})}
