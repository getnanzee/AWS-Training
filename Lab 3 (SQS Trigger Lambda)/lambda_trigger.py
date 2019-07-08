import os
from datetime import datetime
import json
import boto3

DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']
dynamodb = boto3.resource('dynamodb')

def message_queue(event, context):

    print(event)

    table = dynamodb.Table(DYNAMODB_TABLE)

    print('Storing to DynamoDB')

    response = table.put_item(
        Item={
            'MessageId': event['Records'][0]['messageId'],
            'Body': event['Records'][0]['body'],
            'Timestamp': datetime.now().isoformat()
        })

    print("Wrote message to DynamoDB:", json.dumps(response))
