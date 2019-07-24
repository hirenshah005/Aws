import boto3


def create_sns(sns_name):
    """
    A function to create sns
    """
    conn = boto3.client('sns', region_name='ap-south-1')
    # create topic
    response = conn.create_topic(
        Name=sns_name)

    # get arn
    topic_arn = response['TopicArn']

    # subscribe to topic

    response = conn.subscribe(
        TopicArn=topic_arn,
        Protocol='HTTP',
        Endpoint='specify',
    )


create_sns('sns1')
