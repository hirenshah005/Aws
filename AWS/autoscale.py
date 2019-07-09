import json

import boto3


def get_launch_configs(region):
    """
    Function to get all laucnh configs name
    """
    # connect to the instance
    client = boto3.client('autoscaling', region_name=region)
    response = client.describe_launch_configurations()
    # select only launch config key
    response = response['LaunchConfigurations']
    config_name = []
    # Filter all the names
    for i in range(len(response)):
        temp = response[i]
        config_name.append(temp['LaunchConfigurationName'])
    return config_name


def get_auto_scale_groups(region):
    """
    Funtion to get names of autoscale groups
    """
    client = boto3.client('autoscaling', region_name=region)
    response = client.describe_auto_scaling_groups()
    # Selecting the auto scale groups
    response = response['AutoScalingGroups']
    as_grp_names = []
    # Filter all AutoScale Groups
    for i in range(len(response)):
        temp = response[i]
        as_grp_names.append(temp['AutoScalingGroupName'])
    return as_grp_names


def auto_scale_info(region, launch_req, as_req):
    """
    Funtion to Describe the config and autoscale groups fully
    """
    client = boto3.client('autoscaling', region_name=region)
    # selecting the required launch req
    response = client.describe_launch_configurations(
        LaunchConfigurationNames=[launch_req]
    )
    response = response['LaunchConfigurations'][0]
    # selecting only the required keys in the dict
    req_keys = ['LaunchConfigurationName', 'LaunchConfigurationARN', 'ImageId', 'KeyName',
                'SecurityGroups', 'InstanceType', 'BlockDeviceMappings', 'CreatedTime']
    req_info = []
    for k, v in response.items():
        for i in range(len(req_keys)):
            if k == req_keys[i]:
                # append only req key info
                req_info.append(response[k])

    print("Launch Configuration")
    print()
    for i in range(len(req_info)):
        # breaking down Blckdevmap to retrieve only req info
        if req_keys[i] == 'BlockDeviceMappings':
            temp = req_info[i]
            temp = temp[0]
            temp = temp['Ebs']
            print("VolumeSize : {}".format(temp['VolumeSize']))
            print('VolumeType : {}'.format(temp['VolumeType']))
        else:
            print("{0} : {1}".format(req_keys[i], req_info[i]))
    print()

    # Selecting the req as grp
    response = client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[as_req]
    )
    response = response['AutoScalingGroups'][0]
    # Filter the required keys
    req_keys = ['AutoScalingGroupName', 'AutoScalingGroupARN', 'LaunchConfigurationName', 'MinSize', 'MaxSize',
                'AvailabilityZones', 'HealthCheckType', 'HealthCheckGracePeriod', 'Instances', 'VPCZoneIdentifier']
    req_info = []

    for k, v in response.items():
        for i in range(len(req_keys)):
            # appending only req info
            if k == req_keys[i]:
                req_info.append(response[k])

    for i in range(len(req_info)):
        # breaking down instances for only req info
        if req_keys[i] == 'Instances':
            temp = req_info[i]
            temp = temp[0]
            print("Instance ID: {}".format(temp['InstanceId']))
            print('AvailabilityZone : {}'.format((temp['AvailabilityZone'])))
        else:
            print("{0} : {1}".format(req_keys[i], req_info[i]))


def all_launch_info():
    # Connecting to aws
    conn = boto3.client('ec2')
    # List all regions
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    launch_info = []
    auto_scale = []
    for region in regions:
        conn = boto3.client('autoscaling', region_name=region)

        response = conn.describe_launch_configurations()
        response = response['LaunchConfigurations']

        for i in response:
            # selecting only the required keys in the dict
            req_keys = ['LaunchConfigurationName', 'LaunchConfigurationARN', 'ImageId', 'KeyName',
                        'SecurityGroups', 'InstanceType', 'BlockDeviceMappings', 'CreatedTime']
            req_info = []
            for k, v in i.items():
                for j in range(len(req_keys)):
                    if k == req_keys[j]:
                        # append only req key info
                        req_info.append(i[k])
            # launch_info.append(req_info)

            for j in range(len(req_info)):
                # breaking down Blckdevmap to retrieve only req info
                if req_keys[j] == 'BlockDeviceMappings':
                    temp = req_info[j]
                    temp = temp[0]
                    temp = temp['Ebs']
                    del req_info[j]
                    req_info.append(temp['VolumeSize'])
                    req_info.append(temp['VolumeType'])
            launch_info.append(req_info)

            # Selecting the req as grp
        response = conn.describe_auto_scaling_groups()
        response = response['AutoScalingGroups']

        for i in response:
            # Filter the required keys
            req_keys = ['AutoScalingGroupName', 'AutoScalingGroupARN', 'LaunchConfigurationName', 'MinSize', 'MaxSize',
                        'AvailabilityZones', 'HealthCheckType', 'HealthCheckGracePeriod', 'Instances',
                        'VPCZoneIdentifier']
            req_info = []

            for k, v in i.items():
                for j in range(len(req_keys)):
                    # appending only req info
                    if k == req_keys[j]:
                        req_info.append(i[k])

            for j in range(len(req_info)):
                # breaking down instances for only req info
                if req_keys[j] == 'Instances':
                    temp = req_info[j]
                    temp = temp[0]
                    del req_info[j]
                    req_info.append(temp['InstanceId'])
                    req_info.append(temp['AvailabilityZone'])
            auto_scale.append(req_info)
    list_conf = []
    list_auto_scale = []
    req_keys_conf = ['LaunchConfigurationName', 'LaunchConfigurationARN', 'ImageId', 'KeyName',
                     'SecurityGroups', 'InstanceType', 'CreatedTime', 'Volume Size', 'Volume Type']

    req_keys_auto = ['AutoScalingGroupName', 'AutoScalingGroupARN', 'LaunchConfigurationName', 'MinSize', 'MaxSize',
                     'AvailabilityZones', 'HealthCheckType', 'HealthCheckGracePeriod',
                     'VPCZoneIdentifier', 'InstanceId', 'AvailabilityZone']
    for i in launch_info:
        dictionary_conf = dict(zip(req_keys_conf, i))
        list_conf.append(dictionary_conf)
    for i in auto_scale:
        dictionary_auto = dict(zip(req_keys_auto, i))
        list_auto_scale.append(dictionary_auto)

    final_dict_conf = {"LaunchConfiguration": list_conf}
    final_dict_auto = {"AutoScale Groups": list_auto_scale}

    json_conf = json.dumps(final_dict_conf, indent=4, default=str)
    json_auto = json.dumps(final_dict_auto, indent=4, default=str)

    print("Launch Configs")
    print(json_conf)
    print()
    print("json_auto")
    print(json_auto)


# launch_value = get_launch_configs('ap-south-1')
# as_grp_value = get_auto_scale_groups('ap-south-1')
# auto_scale_info('ap-south-1', launch_value[0], as_grp_value[0])
all_launch_info()
