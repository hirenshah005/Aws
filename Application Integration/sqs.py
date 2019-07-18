import boto3
import json


def get_sqs_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    queue_info = []
    for region in regions:
        client = boto3.client('sqs', region_name=region)
        try:
            response = client.list_queues()['QueueUrls']
        except KeyError:
            continue
        queue_names = []

        for res in response:
            queue_names.append(res['QueueUrls'])

        for urls in queue_names:
            response = client.get_queue_attributes(
                QueueUrl=urls
            )
            req_info = []
            req_info.append(response)
            queue_info.append(req_info)

    dict_queue = {'Queue Info': queue_info}

    queue_json = json.dumps(dict_queue,indent=4,default=str)

    print(queue_json)


get_sqs_info()