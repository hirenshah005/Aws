import boto3
import json


def get_key_information():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    key_info = []

    for region in regions:
        client = boto3.client('kms', region_name=region)
        response = client.list_keys()['Keys']
        key_names = []
        for res in response:
            key_names.append(res['KeyId'])

        for ids in key_names:
            response = client.describe_key(
                KeyId=ids
            )['KeyMetadata']
            req_info = []
            req_info.append(response)
            key_info.append(req_info)

    key_dict = {'Keys': key_info}

    key_json = json.dumps(key_dict, indent=4, default=str)

    print(key_json)


get_key_information()
