import boto3
import json


def get_lambda_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    func_info = []
    for region in regions:
        func_names = []
        conn = boto3.client('lambda', region_name=region)
        response = conn.list_functions()
        response = response['Functions']
        for i in response:
            func_names.append(i["FunctionName"])

        for i in func_names:
            func_dets = []
            response = conn.get_function(
                FunctionName=i
            )
            response = response['Configuration']
            req_keys = ['FunctionName', 'FunctionArn', 'Runtime', 'Role', 'CodeSize', 'Description', 'Timeout',
                        'MemorySize', 'LastModified']

            for k in response.keys():
                for l in range(len(req_keys)):
                    if k == req_keys[l]:
                        func_dets.append(response[k])
            func_info.append(func_dets)

    lambda_info = []
    req_keys = ['FunctionName', 'FunctionArn', 'Runtime', 'Role', 'CodeSize', 'Description', 'Timeout',
                'MemorySize', 'LastModified']
    for i in func_info:
        dict_lambda = dict(zip(req_keys, i))
        lambda_info.append(dict_lambda)

    final_dict = {"Lambda Fucntions": lambda_info}
    json_lambda = json.dumps(final_dict, indent=4, default=str)
    print(json_lambda)


get_lambda_info()
