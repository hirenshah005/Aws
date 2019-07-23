import boto3
import json


def get_aws_secret_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    secrets_info = []

    for region in regions:
        if region == 'ap-east-1':
            continue

        client = boto3.client('secretsmanager')
        response = client.list_secrets()['SecretList']

        for res in response:
            req_info = []
            req_info.append(res)
            secrets_info.append(req_info)

    secrets_dict = {"Secrets": secrets_info}

    secrets_json = json.dumps(secrets_dict, indent=4, default=str)

    print(secrets_json)


get_aws_secret_info()
