import boto3
import json


def get_amazon_bridge_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    rule_info = []
    for region in regions:
        client = boto3.client('events', region_name=region)
        response = client.list_rules()['Rules']
        rule_names = []
        for res in response:
            rule_names.append(res['Name'])

        for name in rule_names:
            response = client.describe_rule(
                Name=name,
            )
            req_info = []
            req_info.append(response)
            rule_info.append(req_info)

    rule_dict = {"Rules": rule_info}

    json_rule = json.dumps(rule_dict, indent=4, default=str)

    print(json_rule)


get_amazon_bridge_info()
