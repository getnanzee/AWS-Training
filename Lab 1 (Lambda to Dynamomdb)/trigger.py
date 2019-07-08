import boto3

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):

    create_tables()


def create_tables():

    TableName = 'artist'

    existing_table = dynamodb.list_tables()
    print(existing_table)

    if TableName not in existing_table['TableNames']:

        table = dynamodb.create_table(
        TableName= TableName,
        KeySchema=[
            {
                'AttributeName': 'artistname',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'last_name',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'artistname',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'last_name',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
        )

        if table['TableDescription']['ItemCount'] == 0:
            print('Table Created Successfully')

    else:
        print("Table {} already exist".format(TableName))

    insert_records(TableName)

def insert_records(tablename):

    response = dynamodb.put_item(TableName = tablename, Item={
        'artistname': {'S': 'getnazee'},
        'first_name': {'S': 'Abhishek'},
        'last_name': {'S': 'Sharma'},
        'age': {'N': '25'},
    })
