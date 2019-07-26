import boto3
import json


def get_lightsail_list():
    """
    Function to get all lightsail names
    """
    conn = boto3.client('lightsail')
    regions = [region['name'] for region in conn.get_regions()['regions']]
    instance_names = []
    for region in regions:
        client = boto3.client('lightsail',region_name=region)
        all_instance = client.get_instances()
        instances = []
        # get all instance info
        for k, v in all_instance.items():
            if k == 'instances':
                instances.append(all_instance[k])
        instances = instances[0]
        # get the lightsail names
        for i in range(0, len(instances)):
            select_instance = instances[i]
            for k, v in select_instance.items():
                if k == 'name':
                    instance_names.append(select_instance[k])
    return instance_names


def lightsail_details(region, instance_name):
    """
    A function to get lightsail information
    """
    client = boto3.client('lightsail', region_name=region)
    # selecting the required lighstail name
    instance_info = client.get_instance(
        instanceName=instance_name
    )
    # Refining the response
    instance_info = instance_info['instance']
    req_info_list = []
    req_info = ['name', 'arn', 'location', 'blueprintId', 'bundleId', 'publicIpAddress', 'hardware', 'sshKeyName']
    for k, v in instance_info.items():
        for i in range(0, len(req_info)):
            if k == req_info[i]:
                req_info_list.append(instance_info[k])

    for i in range(0, (len(req_info))):
        # refining the spec key for finer info
        if req_info[i] == 'hardware':
            temp = req_info_list[6]
            print("cpuCount:{}".format(temp['cpuCount']))
            print("ramSizeInGb:{}".format(temp['ramSizeInGb']))
        else:
            print('{0} : {1}'.format(req_info[i], req_info_list[i]))


def get_all_lightsail_info():
    """
    A function to get every lightsail info across all regions
    """
    conn = boto3.client('lightsail')
    regions = [region['name'] for region in conn.get_regions()['regions']]
    lightsail_info = []
    for region in regions:
        instance_names = []
        client = boto3.client('lightsail', region_name=region)
        all_instance = client.get_instances()
        instances = []
        # get all instance info
        for k, v in all_instance.items():
            if k == 'instances':
                instances.append(all_instance[k])
        instances = instances[0]
        # get the lightsail names
        for i in range(0, len(instances)):
            select_instance = instances[i]
            for k, v in select_instance.items():
                if k == 'name':
                    instance_names.append(select_instance[k])

        # get the instance info
        for j in instance_names:
            instance_info = client.get_instance(
                instanceName=j
            )
            # Refining the response
            instance_info = instance_info['instance']
            req_info_list = []
            req_info = ['name', 'arn', 'location', 'blueprintId', 'bundleId', 'publicIpAddress', 'hardware',
                        'sshKeyName']
            for k, v in instance_info.items():
                for i in range(0, len(req_info)):
                    if k == req_info[i]:
                        req_info_list.append(instance_info[k])

            for i in range(0, (len(req_info))):
                # refining the spec key for finer info
                if req_info[i] == 'hardware':
                    temp = req_info_list[6]
                    del req_info_list[i]
                    req_info_list.append(temp['cpuCount'])
                    req_info_list.append(temp['ramSizeInGb'])
            lightsail_info.append(req_info_list)

    lightsail_list = []
    # required keys for final list
    req_info = ['name', 'arn', 'location', 'blueprintId', 'bundleId', 'publicIpAddress', 'hardware',
                'sshKeyName']

    # convert list into dictionary
    for i in lightsail_info:
        dict_lightsail = dict(zip(req_info,i))
        lightsail_list.append(dict_lightsail)

    # final dict to convert to json
    final_dict = {"Lightsail":lightsail_list}

    # cnvert dicionary to json
    json_final = json.dumps(final_dict, indent=4,default=str)
    print(json_final)


#
# instance_names = get_lightsail_list()
# # lightsail_details('ap-south-1', value[0])
get_all_lightsail_info()
