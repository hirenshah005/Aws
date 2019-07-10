import boto3
import json


#     list_inst = []
#     for i in instance_list:
#         dictionary = dict(zip(instance_list_info, i))
#         list_inst.append(dictionary)
#
#     final_dict = {"Instances": list_inst}
#     json_final = json.dumps(final_dict, indent=4)
#     print(json_final)


def get_all_instance_desc():
    """
    Function that lists and describes all instance info
    """
    # Connecting to aws
    conn = boto3.client('ec2')
    # List all regions
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    instance_info = []
    # check for elastic Ip
    elastic_check = False
    # Iterating through all regions
    for region in regions:

        conn = boto3.client('ec2', region_name=region)
        # Describing all instances
        response = conn.describe_instances()
        # Selecting  all required keys from the function
        req_info = ['Reservations', 'Placement', 'PublicIpAddress', 'SubnetId', 'SubnetId']
        req_info_list = []
        req_info_list_refined = []
        # Getting the values of keys of req_info
        for k, v in response.items():
            for i in range(0, len(req_info)):
                if k == req_info[i]:
                    req_info_list.append(response[k])
        # Since its stored as a list unwrapping the list
        req_info_list = req_info_list[0]
        # Refining more to get only instance information
        for ins in req_info_list:
            more_filters = ['Instances']
            for k in ins.keys():
                for i in range(0, len(more_filters)):
                    if k == more_filters[i]:
                        req_info_list_refined.append(ins[k])
        # Refining instance info to get only select information
        # iterating throught the refined list
        for j in req_info_list_refined:
            temp = j
            temp = temp[0]
            # information requried from each instance
            req_keys = ['ImageId', 'InstanceId', 'InstanceType', 'LaunchTime', 'Placement', 'PublicIpAddress',
                        'SubnetId', 'VpcId',
                        'NetworkInterfaces',
                        ]
            # Unwrapping the list
            instance_state = temp['State']
            instance_state = instance_state['Name']
            req_info = []

            for k in temp.keys():
                for i in range(len(req_keys)):
                    if k == req_keys[i]:
                        req_info.append(temp[k])

            # Removing Network interface info and only checking for elastic IP
            if instance_state == 'stopped':
                del req_info[-1]
                req_info.append("Instance stopped")

            elif instance_state == 'running':
                temp = req_info[-1]
                temp = temp[0]
                temp = temp['Association']
                if temp['IpOwnerId'] == 'amazon':
                    elastic_check = False
                else:
                    elastic_check = True
                del req_info[-1]
                req_info.append(elastic_check)
            # Appending final info to the req list
            instance_info.append(req_info)
    # print(instance_info)


get_all_instance_desc()
