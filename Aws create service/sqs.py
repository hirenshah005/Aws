import boto3


def create_queue(queue_name):
    conn = boto3.client('sqs', region_name='ap-south-1')
    response = conn.create_queue(
        QueueName=queue_name
    )
    queue_url = response['QueueUrl']
    response = conn.send_message(
        QueueUrl=queue_url,
        MessageBody='Enter your msg here',
        DelaySeconds=10
    )


create_queue("queue1")
