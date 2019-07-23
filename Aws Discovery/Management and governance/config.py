import boto3
import json


def get_aws_config_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    config_rules = []
    delivery_channels = []
    # org_config_rules = []
    for region in regions:
        client = boto3.client('config', region_name=region)
        response = client.describe_config_rules()['ConfigRules']

        for res in response:
            req_info = []
            req_info.append(res)
            config_rules.append(req_info)

        response = client.describe_delivery_channels()['DeliveryChannels']

        for res in response:
            req_info = []
            req_info.append(res)
            delivery_channels.append(req_info)

        # response = client.describe_organization_config_rules()
        #
        # for res in response:
        #     req_info = []
        #     req_info.append(res)
        #     org_config_rules.append(req_info)

    dict_config_rules = {"Configuration Rules": config_rules}
    dict_delivery_channels = {"Delivery Channels": delivery_channels}
    # dict_organization_rules = {"Organization Rules ": org_config_rules}

    json_config_rules = json.dumps(dict_config_rules, indent=4, default=str)
    json_delivery_channels = json.dumps(dict_delivery_channels, indent=4, default=str)
    # json_org_rules = json.dumps(dict_organization_rules, indent=4, default=str)

    print(json_config_rules)
    print(json_delivery_channels)
    # print(json_org_rules)

get_aws_config_info()