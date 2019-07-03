import boto3


def get_lightsail_list(region):
    """
    Function to get all lightsail names
    """
    client = boto3.client('lightsail', region_name=region)
    all_instance = client.get_instances()
    instances = []
    # get all instance info
    for k, v in all_instance.items():
        if k == 'instances':
            instances.append(all_instance[k])
    instances = instances[0]
    instance_names = []
    # get the lightsail names
    for i in range(0, len(instances)):
        select_instance = instances[i]
        for k, v in select_instance.items():
            if k == 'name':
                instance_names.append(select_instance[k])
    return instance_names


def lightsail_details(region, instance_name):
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


value = get_lightsail_list('ap-south-1')
lightsail_details('ap-south-1', value[0])
