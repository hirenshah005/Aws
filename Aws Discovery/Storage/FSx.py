import boto3
import botocore
import json


def get_fsx_info():
    """
    A function that gives fsx file sytems info
    """
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    fsx_info = []

    for region in regions:
        # not available in these regions
        if region == 'us-west-1' or region == 'ap-east-1' or region == 'ap-south-1' or region == 'ap-northeast-1' or region == 'ca-central-1' or region == 'eu-west-3' or region == 'eu-north-1' or region == 'sa-east-1' or region == 'ap-northeast-2':
            continue
        conn = boto3.client('fsx', region_name=region)
        # get file system information
        response = conn.describe_file_systems()['FileSystems']
        for res in response:
            req_info = []
            req_info.append(res)
            fsx_info.append(req_info)

    # convert fsx list into dictionary
    dict_fsx = {"FSX info": fsx_info}

    # convert dictionary into json
    fsx_json = json.dumps(dict_fsx, indent=4, default=str)

    print(fsx_json)


get_fsx_info()
