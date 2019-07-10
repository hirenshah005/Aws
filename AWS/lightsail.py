import boto3


def get_lightsail_list():
    """
    Function to get all lightsail names
    """
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    instance_names = []
    for region in regions:
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
    print(instance_names)
    # return instance_names


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


def get_all_lightsail_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    light_sail = []
    for region in regions:
        conn = boto3.client('lightsail', region_name=region)
        instance_info = conn.get_instance()
        instance_info = instance_info['instance']

        for z in instance_info:
            req_info_list = []
            req_info = ['name', 'arn', 'location', 'blueprintId', 'bundleId', 'publicIpAddress', 'hardware',
                        'sshKeyName']
            for k, v in z.items():
                for i in range(0, len(req_info)):
                    if k == req_info[i]:
                        req_info_list.append(z[k])
            light_sail.append(req_info_list)

            for i in range(0, (len(req_info))):
                # refining the spec key for finer info
                if req_info[i] == 'hardware':
                    temp = req_info_list[6]
                    del light_sail[i]
                    req_info_list.append(temp['cpuCount'])
                    req_info_list.append(temp['ramSizeInGb'])
    print(light_sail)


#
value = get_lightsail_list()
# # lightsail_details('ap-south-1', value[0])
# get_all_lightsail_info()
