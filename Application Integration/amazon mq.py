import boto3
import json


def get_mq_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    broker_info = []

    for region in regions:
        if region == 'eu-north-1' or region == 'sa-east-1':
            continue
        client = boto3.client('mq', region_name=region)
        response = client.list_brokers()['BrokerSummaries']
        broker_names = []
        for res in response:
            broker_names.append(res['BrokerId'])

        for name in broker_names:
            response = client.describe_broker(
                BrokerId=name
            )
            req_info = []
            req_info.append(response)
            broker_info.append(req_info)

    dict_broker = {"Brokers": broker_info}

    json_broker = json.dumps(dict_broker, indent=4, default=str)

    print(json_broker)


get_mq_info()
