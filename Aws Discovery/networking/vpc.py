import boto3
import json


# def vpc_info(region):
#     conn = boto3.resource('ec2', region_name=region)
#     ec2 = boto3.client('ec2', region_name=region)
#     vpc_dict = ec2.describe_vpcs()
#     vpc_list = vpc_dict['Vpcs']
#     vpc_req_info = vpc_list[0]
#     vpc_req_options = ['CidrBlock', 'VpcId']
#     vpc_info = []
#
#     for k, v in vpc_req_info.items():
#         for i in range(0, len(vpc_req_options)):
#             if k == vpc_req_options[i]:
#                 vpc_info.append(vpc_req_info[k])
#
#     instance_ids = list(conn.instances.filter(InstanceIds=[]))
#     req_id = list(conn.instances.filter(Filters=[{'Name': 'instance-id', 'Values': ['i-0fca6b6238e831f79']}]))
#     subnet_id = req_id[0].subnet
#
#     for i in range(0, len(vpc_req_options)):
#         print('{0} : {1}'.format(vpc_req_options[i], vpc_info[i]))
#     print(subnet_id)


def get_all_vpc_info():
    """
    A fucntion that gives vpc information
    """
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    vpc_info = []
    for region in regions:
        req_info = []
        conn = boto3.client('ec2', region_name=region)
        # get vpc info
        response = conn.describe_vpcs()['Vpcs']
        for res in response:
            req_info.append(res)
        vpc_info.append(req_info)
    # convert vpc list to dictionary
    final_dict = {"VPC Ids": vpc_info}
    # convert dictionary to json
    json_final = json.dumps(final_dict, indent=4, default=str)
    print(json_final)


# vpc_info("ap-south-1")
get_all_vpc_info()
