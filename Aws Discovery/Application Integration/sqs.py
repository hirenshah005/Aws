import boto3
import json


def get_sqs_info():
    """
    Get sqs Queue information
    """
    # usin ec2 to get region info
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    queue_info = []
    # looping through the regions
    for region in regions:
        client = boto3.client('sqs', region_name=region)
        # try catch to get empty lists
        try:
            response = client.list_queues()['QueueUrls']
        except KeyError:
            continue
        queue_names = []
        # Getting the queue names
        for res in response:
            queue_names.append(res['QueueUrls'])

        # Get the queue atrributes
        for urls in queue_names:
            response = client.get_queue_attributes(
                QueueUrl=urls
            )
            req_info = []
            req_info.append(response)
            # seperate lists for seperating info
            queue_info.append(req_info)

    # converting into a dictionary for final processing
    dict_queue = {'Queue Info': queue_info}

    # Convert to json
    queue_json = json.dumps(dict_queue,indent=4,default=str)

    print(queue_json)


get_sqs_info()