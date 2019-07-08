import boto3

VERIFIED_EMAIL = 'abhishek.replies@gmail.com'

ses = boto3.client('ses')
sns = boto3.client('sns')
def lambda_handler(event, context):

    print(event)

    ses.send_email(
        Source=VERIFIED_EMAIL,
        Destination={
            'ToAddresses': [event['email']]  # Also a verified email
        },
        Message={
            'Subject': {'Data': 'A reminder from your reminder service!'},
            'Body': {'Text': {'Data': event['message']}}
        }
    )

    response = ses.list_identities(MaxItems=10)
    print(response)

    sns.publish(PhoneNumber=event['phone'], Message=event['message'])
    return 'Success!'
