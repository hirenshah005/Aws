import boto3
import json


def get_global_aclrtr_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    acc_info = []
    # for region in regions:
    #     if region == 'eu-north-1' or region == 'ap-south-1' or region == 'eu-west-3' or region == 'eu-west-2' or region == 'eu-west-1' or region == 'ap-northeast-2' or region == 'ap-northeast-1' or region == 'sa-east-1' or region == 'ca-central-1':
    #         continue
    conn = boto3.client('globalaccelerator', region_name='us-west-2')
    response = conn.list_accelerators()['Accelerators']
    acc_names = []
    for res in response:
        acc_names.append(res['AcceleratorArn'])

    for name in acc_names:
        response = conn.describe_accelerator(
            AcceleratorArn=name
        )['Accelerator']
        req_info = []
        for res in response:
            req_info.append(res)
        acc_info.append(req_info)

    final_dict = {"Accelators": acc_info}
    json_aclrtr = json.dumps(final_dict, indent=4, default=str)
    print(json_aclrtr)


get_global_aclrtr_info()
