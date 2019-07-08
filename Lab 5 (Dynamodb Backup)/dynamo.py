import datetime
import boto3, os

#https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Operations_Amazon_DynamoDB.html

MAX_BACKUP = os.environ['MAX_BACKUP']
MAX_BACKUP = int(MAX_BACKUP)

dynamodb = boto3.client('dynamodb')

def db_backup(event, context):

    if 'TableName' not in event:
        raise Exception("No table name specified")

    table_name = event['TableName']

    create_backup(table_name)
    delete_backups(table_name)


def create_backup(table_name):
    print("Backing up table: ", table_name)

    backup_name = table_name + '-' + datetime.datetime.now().strftime('%y%m%d%H%M%S')

    response = dynamodb.create_backup(TableName=table_name, BackupName=backup_name)

    print(response)


def delete_backups(table_name):
    print("Deleting old backups from ", table_name)

    backups = dynamodb.list_backups(TableName=table_name)

    backup_count = len(backups['BackupSummaries'])
    print('Total backup count: ', backup_count)

    if backup_count <= MAX_BACKUP:
        print('No stale backups')
        return

    sorted_list = sorted(backups['BackupSummaries'], key= lambda k: k['BackupCreationDateTime'])

    old_backups = sorted_list[:MAX_BACKUP]

    for backup in old_backups:
        arn = backup['BackupArn']
        print('ARN to delete: ' + arn)
        delete_arn = dynamodb.delete_backup(BackupArn=arn)
        status = delete_arn['BackupDescription']['BackupDetails']['BackupStatus']

        print('Status: ', status)
