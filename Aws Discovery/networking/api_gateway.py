import boto3
import json


def get_api_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]

    for region in regions:
        conn = boto3.client('apigateway', region_name=region)
        response = conn.get_rest_apis()['items']
        for res in response:
            print(res['id'])
        # id = response['id']
        # print(id)
        # ids = response['id']
        # response = conn.get_deployments(
        #     restApiId=ids
        # )
        # print(response)


get_api_info()
