import boto3
import json


def get_aws_org_info():
    """
    A function that returns accounts policies and organization info
    """
    client = boto3.client('organizations')
    # list all the accounts
    response = client.list_accounts()
    account_info = []
    policy_info = []
    org_info = []

    req_info = []
    # append account info
    for res in response:
        req_info.append(res)
    account_info.append(req_info)

    # get all the accont policies
    response = client.client.list_policies()
    req_info = []
    # append the poilicies
    for res in response:
        req_info.append(res)
    policy_info.append(req_info)

    # get the organization info
    response = client.describe_organization()
    req_info = []
    # append the organization info
    for res in response:
        req_info.append(res)
    org_info.append(req_info)

    # convert accounts policies and organization info to dictionary
    dict_account = {"Account": account_info}
    dict_policy = {"Policy": policy_info}
    dict_org = {"Organization": org_info}

    # convert dictionaries into json
    json_acc = json.dumps(dict_account, indent=4, default=str)
    json_policy = json.dumps(dict_policy, indent=4, default=str)
    json_org = json.dumps(dict_org, indent=4, default=str)

    print(json_acc)
    print(json_policy)
    print(json_org)


get_aws_org_info()
