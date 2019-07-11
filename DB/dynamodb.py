import boto3
import json


def get_dynamodb_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    table_info = []
    req_keys = []
    for region in regions:
        conn = boto3.client('dynamodb', region_name=region)
        response = conn.list_tables()['TableNames']

        for res in response:
            req_keys = []
            req_info = []
            response = conn.describe_table(
                TableName=res
            )['Table']
            for k in response.keys():
                req_keys.append(k)
                req_info.append(response[k])
            table_info.append(req_info)

    dynamo_list = []

    for i in table_info:
        dict_dynamo = dict(zip(req_keys, i))
        dynamo_list.append(dict_dynamo)

    final_dynamo = {"DynamoDb": dynamo_list}
    json_dynamo = json.dumps(final_dynamo, indent=4, default=str)

    print(json_dynamo)


get_dynamodb_info()
