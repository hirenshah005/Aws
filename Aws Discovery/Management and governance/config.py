import boto3
import json


def get_aws_config_info():
    """
    A function that gets aws config rules and delivery channels
    """
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    config_rules = []
    delivery_channels = []
    # org_config_rules = []
    for region in regions:
        client = boto3.client('config', region_name=region)
        # get the configuration rules
        response = client.describe_config_rules()['ConfigRules']

        # append the config info
        for res in response:
            req_info = []
            req_info.append(res)
            config_rules.append(req_info)

        # get delivery channels info
        response = client.describe_delivery_channels()['DeliveryChannels']

        # append the delivery channels info
        for res in response:
            req_info = []
            req_info.append(res)
            delivery_channels.append(req_info)

        # returing a error
        # response = client.describe_organization_config_rules()
        #
        # for res in response:
        #     req_info = []
        #     req_info.append(res)
        #     org_config_rules.append(req_info)

    # covertt the config rules and delivery channels to dictionary
    dict_config_rules = {"Configuration Rules": config_rules}
    dict_delivery_channels = {"Delivery Channels": delivery_channels}
    # dict_organization_rules = {"Organization Rules ": org_config_rules}

    # convert the dictionaries into json
    json_config_rules = json.dumps(dict_config_rules, indent=4, default=str)
    json_delivery_channels = json.dumps(dict_delivery_channels, indent=4, default=str)
    # json_org_rules = json.dumps(dict_organization_rules, indent=4, default=str)

    print(json_config_rules)
    print(json_delivery_channels)
    # print(json_org_rules)


get_aws_config_info()
