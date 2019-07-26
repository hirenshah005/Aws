import boto3
import json


def get_hsm_info():
    """
    A fucntion that gives hsm information
    """
    conn = boto3.client('cloudhsm', region_name='us-west-2')
    hsm_info = []
    # get hsm info
    response = conn.describe_hsm()
    for res in response:
        req_info = []
        req_info.append(res)
        hsm_info.append(res)

    # convert hsm list into dictionary
    hsm_dict = {"HSM": hsm_info}

    # convert dictionary into json
    hsm_json = json.dumps(hsm_dict, indent=4, default=str)

    print(hsm_json)


get_hsm_info()
