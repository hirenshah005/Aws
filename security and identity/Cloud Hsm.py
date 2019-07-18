import boto3
import json


def get_hsm_info():
    conn = boto3.client('cloudhsm', region_name='us-west-2')
    hsm_info = []
    response = conn.describe_hsm()
    for res in response:
        req_info = []
        req_info.append(res)
        hsm_info.append(res)

    hsm_dict = {"HSM":hsm_info}
    hsm_json = json.dumps(hsm_dict,indent=4,default=str)

    print(hsm_json)


get_hsm_info()
