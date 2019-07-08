import boto3

VERIFIED_EMAIL  = 'abhishek.replies@gmail.com'
ses = boto3.client('ses')

def lambda_handler(event, context):

    print(event)

    for i in event["Records"]:
        action = i['eventName']
        bucket_name = i['s3']['bucket']['name']
        object = i['s3']['object']['key']

        subject = str(action) + 'event from' + bucket_name
        body = """Test mail - for S3 trigger {} event and {} object""".format(action,object)

        message = {"Subject": {'Data': subject},
                    'Body': {'Text': {'Data': body}}}

        response = ses.send_email(Source =VERIFIED_EMAIL,
                                Destination = {'ToAddresses': ['abhishek.replies@gmail.com']}, Message = message)

        print(response)
