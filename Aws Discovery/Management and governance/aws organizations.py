import boto3
import json


def get_aws_org_info():
    client = boto3.client('organizations')
    response = client.list_accounts()
    account_info = []
    policy_info = []
    org_info = []

    req_info = []
    for res in response:
        req_info.append(res)
    account_info.append(req_info)

    response = client.client.list_policies()
    req_info = []
    for res in response:
        req_info.append(res)
    policy_info.append(req_info)

    response = client.describe_organization()
    req_info = []
    for res in response:
        req_info.append(res)
    org_info.append(req_info)

    dict_account = {"Account": account_info}
    dict_policy = {"Policy": policy_info}
    dict_org = {"Organization": org_info}

    json_acc = json.dumps(dict_account, indent=4, default=str)
    json_policy = json.dumps(dict_policy, indent=4, default=str)
    json_org = json.dumps(dict_org, indent=4, default=str)

    print(json_acc)
    print(json_policy)
    print(json_org)

get_aws_org_info()