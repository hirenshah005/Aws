import boto3


def create_launch_config(conig_name, image_id, inst_type):
    """
    A function to create a launch configuration
    """
    client = boto3.client('autoscaling', region_name='ap-south-1')
    # creating the launch configuration
    response = client.create_launch_configuration(
        LaunchConfigurationName=conig_name,
        ImageId=image_id,
        InstanceType=inst_type,
        InstanceMonitoring={
            'Enabled': False
        },
        EbsOptimized=False,
        AssociatePublicIpAddress=True,
    )
    # return the config name for creating auto scale group
    return conig_name


def create_auto_scale_group(auto_scale_name):
    """
    A function to create auto scale groups
    """
    client = boto3.client('autoscaling', region_name='ap-south-1')
    # call the launch config func
    conf_name = create_launch_config("lc1", 'ami-0d2692b6acea72ee6', 't2.micro')

    # creating the auto scale groups
    response = client.create_auto_scaling_group(
        AutoScalingGroupName=auto_scale_name,
        LaunchConfigurationName=conf_name,
        MinSize=1,
        MaxSize=1,
        VPCZoneIdentifier='subnet-9e56ecd2'
    )


create_auto_scale_group('as1')
