import boto3
import json


# Resource access manager(ram)
def get_ram_info():
    """
    A function that gives ram resource shares info and resource associations
    """
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    shares_info = []
    share_principles = []
    share_resources = []

    for region in regions:
        # not available in this regions
        if region == 'ap-east-1' or region == 'eu-north-1' or region == 'sa-east-1':
            continue

        conn = boto3.client('ram', region_name=region)
        # get resource shares info
        response = conn.get_resource_shares(
            resourceOwner='SELF'
        )['resourceShares']
        for res in response:
            req_info = []
            req_info.append(res)
            shares_info.append(req_info)

        # get resource associations that are principal
        response = conn.get_resource_share_associations(
            associationType='PRINCIPAL'
        )['resourceShareAssociations']
        for res in response:
            req_info = []
            req_info.append(res)
            share_principles.append(req_info)

        # get resource associations that are resource
        response = conn.get_resource_share_associations(
            associationType='RESOURCE'
        )['resourceShareAssociations']

        for res in response:
            req_info = []
            req_info.append(res)
            share_resources.append(req_info)

    # convert all shares list into dictionaries
    shares_dict = {"Shares": shares_info}
    share_resource_dict = {"Share Resources": share_resources}
    share_principle_dict = {"Share Principles": share_principles}

    # convert dicitonaries into json
    shares_json = json.dumps(shares_dict, indent=4, default=str)
    share_resource_json = json.dumps(share_resource_dict, indent=4, default=str)
    share_principle_json = json.dumps(share_principle_dict, indent=4, default=str)

    print(shares_json)
    print(share_resource_json)
    print(share_principle_json)


get_ram_info()
