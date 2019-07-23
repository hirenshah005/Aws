import boto3
import json


def get_license_management_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    license_info = []

    for region in regions:
        client = boto3.client('license-manager', region_name=region)
        response = client.list_license_configurations()

        for res in response:
            req_info = []
            req_info.append(res)
            license_info.append(req_info)

    dict_license = {"Liceneses": license_info}

    json_license = json.dumps(dict_license, indent=4, default=str)

    print(json_license)


get_license_management_info()
