import boto3
import json


def get_security_hub_info():
    """
    A fucntion that gives security hub products info
    """

    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    product_info = []

    for region in regions:
        # not availble in this region
        if region == 'ap-east-1':
            continue

        client = boto3.client('securityhub', region_name=region)
        # get product information
        response = client.describe_products()['Products']

        for res in response:
            req_info = []
            req_info.append(res)
            product_info.append(req_info)

    # convert products list into dictionary
    product_dict = {"Products": product_info}

    # convert dictionary into json
    products_json = json.dumps(product_dict, indent=4, default=str)

    print(products_json)


get_security_hub_info()
