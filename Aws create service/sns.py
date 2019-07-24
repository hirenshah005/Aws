import boto3


def create_sns(sns_name):
    conn = boto3.client('sns', region_name='ap-south-1')
    response = conn.create_topic(
        Name=sns_name)

    topic_arn = response['TopicArn']
    response = conn.subscribe(
        TopicArn=topic_arn,
        Protocol='HTTP',
        Endpoint='specify',
    )


create_sns('sns1')
