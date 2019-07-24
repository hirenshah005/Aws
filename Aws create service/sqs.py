import boto3


def create_queue(queue_name):
    """
    A function to create a queue
    """
    conn = boto3.client('sqs', region_name='ap-south-1')
    # create queue
    response = conn.create_queue(
        QueueName=queue_name
    )
    #   get url
    queue_url = response['QueueUrl']

    # send the message
    response = conn.send_message(
        QueueUrl=queue_url,
        MessageBody='Enter your msg here',
        DelaySeconds=10
    )


create_queue("queue1")
