import boto3
import json


def get_directory_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    directory_info = []

    for region in regions:
        if region == 'ap-east-1' or region == 'eu-west-3':
            continue

        conn = boto3.client('ds', region_name=region)
        response = conn.describe_directories()['DirectoryDescriptions']

        for res in response:
            req_info = []
            req_info.append(res)
            directory_info.append(req_info)

    directory_dict = {"Directories": directory_info}
    directory_json = json.dumps(directory_dict, indent=4, default=str)

    print(directory_json)


get_directory_info()
