import boto3
import json


def get_amazon_bridge_info():
    """
    functiond that describes the rules of amazon bridge
    """
    #  selecting ec2 as it contains all the regiona
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    rule_info = []
    # looping through all regions
    for region in regions:
        client = boto3.client('events', region_name=region)
        #   listing all the rules so to get rule names
        response = client.list_rules()['Rules']
        rule_names = []
        for res in response:
            #   appending only names from response
            rule_names.append(res['Name'])

        for name in rule_names:
            #   describe each rule
            response = client.describe_rule(
                Name=name,
            )
            req_info = []
            req_info.append(response)
            #   appending to seperate list as seperate arrays
            rule_info.append(req_info)

    #   forming final dictionary
    rule_dict = {"Rules": rule_info}

    # convert to json
    json_rule = json.dumps(rule_dict, indent=4, default=str)

    print(json_rule)


get_amazon_bridge_info()
