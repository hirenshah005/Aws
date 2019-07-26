import boto3
import json


def get_macie_info():
    """
    A fucntion that gives macie member accounts and its s3 resources
    """
    client = boto3.client('macie', region_name='us-east-1')
    accounts = []
    s3_info = []
    # get all member accounts info
    response = client.list_member_accounts()

    for res in response:
        req_info = []
        req_info.append(res)
        accounts.append(req_info)

    # get s3 resources assoaciated with the user
    response = client.list_s3_resources()

    for res in response:
        req_info = []
        req_info.append(res)
        s3_info.append(req_info)

    # convert user list to dictionary
    accounts_dict = {"Member accounts": accounts}
    s3_info_dict = {"S3 Information": s3_info}

    # convert dicitonaries into json
    accounts_json = json.dumps(accounts_dict, indent=4, default=str)
    s3_json = json.dumps(s3_info_dict, indent=4, default=str)

    print(accounts_json)
    print(s3_json)


get_macie_info()
