import boto3
import json


def get_dynamodb_info():
    """
    A funtion to get dynamodb table info
    """
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    table_info = []
    req_keys = []
    for region in regions:
        conn = boto3.client('dynamodb', region_name=region)
        # get all dynamo tables
        response = conn.list_tables()['TableNames']

        for res in response:
            req_keys = []
            req_info = []
            # get table info of each table
            response = conn.describe_table(
                TableName=res
            )['Table']
            # append to final list
            for k in response.keys():
                req_keys.append(k)
                req_info.append(response[k])
            table_info.append(req_info)

    dynamo_list = []
    # convert dynamo list to dictionary
    for i in table_info:
        dict_dynamo = dict(zip(req_keys, i))
        dynamo_list.append(dict_dynamo)

    # final dictinary
    final_dynamo = {"DynamoDb": dynamo_list}
    # convert dictionary to json
    json_dynamo = json.dumps(final_dynamo, indent=4, default=str)

    print(json_dynamo)


get_dynamodb_info()
