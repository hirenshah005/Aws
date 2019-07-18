import boto3
import json


def get_security_hub_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    product_info = []

    for region in regions:
        if region == 'ap-east-1':
            continue

        client = boto3.client('securityhub', region_name=region)
        response = client.describe_products()['Products']

        for res in response:
            req_info = []
            req_info.append(res)
            product_info.append(req_info)

    product_dict = {"Products": product_info}

    products_json = json.dumps(product_dict, indent=4, default=str)

    print(products_json)


get_security_hub_info()
