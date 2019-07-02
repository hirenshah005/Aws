import boto3


def get_launch_configs(region):
    client = boto3.client('autoscaling', region_name=region)
    response = client.describe_launch_configurations()
    response = response['LaunchConfigurations']
    config_name = []
    for i in range(len(response)):
        temp = response[i]
        config_name.append(temp['LaunchConfigurationName'])
    return config_name


def get_auto_scale_groups(region):
    client = boto3.client('autoscaling', region_name=region)
    response = client.describe_auto_scaling_groups()
    response = response['AutoScalingGroups']
    as_grp_names = []
    for i in range(len(response)):
        temp = response[i]
        as_grp_names.append(temp['AutoScalingGroupName'])
    return as_grp_names


def auto_scale_info(region, launch_req, as_req):
    client = boto3.client('autoscaling', region_name=region)
    response = client.describe_launch_configurations(
        LaunchConfigurationNames=[launch_req]
    )
    response = response['LaunchConfigurations'][0]

    req_keys = ['LaunchConfigurationName', 'LaunchConfigurationARN', 'ImageId', 'KeyName',
                'SecurityGroups', 'InstanceType', 'BlockDeviceMappings', 'CreatedTime']
    req_info = []
    for k, v in response.items():
        for i in range(len(req_keys)):
            if k == req_keys[i]:
                req_info.append(response[k])

    print("Launch Configuration")
    print()
    for i in range(len(req_info)):
        if req_keys[i] == 'BlockDeviceMappings':
            temp = req_info[i]
            temp = temp[0]
            temp = temp['Ebs']
            print("VolumeSize : {}".format(temp['VolumeSize']))
            print('VolumeType : {}'.format(temp['VolumeType']))
        else:
            print("{0} : {1}".format(req_keys[i], req_info[i]))
    print()

    response = client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[as_req]
    )
    response = response['AutoScalingGroups'][0]
    req_keys = ['AutoScalingGroupName', 'AutoScalingGroupARN', 'LaunchConfigurationName', 'MinSize', 'MaxSize',
                'AvailabilityZones', 'HealthCheckType', 'HealthCheckGracePeriod', 'Instances', 'VPCZoneIdentifier']
    req_info = []
    print("Auto_scale_info")
    print()
    for k, v in response.items():
        for i in range(len(req_keys)):
            if k == req_keys[i]:
                req_info.append(response[k])

    for i in range(len(req_info)):
        if req_keys[i] == 'Instances':
            temp = req_info[i]
            temp = temp[0]
            print("Instance ID: {}".format(temp['InstanceId']))
            print('AvailabilityZone : {}'.format((temp['AvailabilityZone'])))
        else:
            print("{0} : {1}".format(req_keys[i], req_info[i]))


launch_value = get_launch_configs('ap-south-1')
as_grp_value = get_auto_scale_groups('ap-south-1')
auto_scale_info('ap-south-1', launch_value[0], as_grp_value[0])
