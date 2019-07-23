import boto3
import json


def get_mq_info():
    """
    Function to get Amazon mq broker data
    """
    #   choosing ec2 to get region info
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    broker_info = []
    #   looping through regions
    for region in regions:
        if region == 'eu-north-1' or region == 'sa-east-1':
            continue
        client = boto3.client('mq', region_name=region)
        #   listing brokers to get broker name for describe
        response = client.list_brokers()['BrokerSummaries']
        broker_names = []
        for res in response:
            broker_names.append(res['BrokerId'])

        for name in broker_names:
            # Describing each broker
            response = client.describe_broker(
                BrokerId=name
            )
            req_info = []
            req_info.append(response)
            # appending to seperate list to get seperated broker info
            broker_info.append(req_info)

    # getting the final dictionary
    dict_broker = {"Brokers": broker_info}
    #   convert to json
    json_broker = json.dumps(dict_broker, indent=4, default=str)

    print(json_broker)


get_mq_info()
