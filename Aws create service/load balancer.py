import boto3


def create_loadbalancer(lb_name, app_type):
    """
    A fucntion to create load balancer
    """
    client = boto3.client('elbv2', region_name='ap-south-1')
    conn = boto3.client('ec2', region_name='ap-south-1')
    # get subnets to create load balancer (Min=3)
    response = conn.describe_subnets()['Subnets']
    subnets = []

    for res in response:
        subnets.append(res['SubnetId'])
    # create the load balancer
    response = client.create_load_balancer(
        Name=lb_name,
        Subnets=subnets,
        Type=app_type
    )['LoadBalancers']

    # get load balancer arn to create the target group
    lb_arn = response[0]['LoadBalancerArn']
    # create the targer group
    tg_arn = create_target_group('tg1')

    # create the listener that points to the target group
    response = client.create_listener(
        LoadBalancerArn=lb_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': tg_arn
            }
        ],
    )


def create_target_group(tg_name):
    """
    A function to create the target group
    """
    tg = boto3.client('elbv2', region_name='ap-south-1')
    # create the target groups
    response = tg.create_target_group(
        Name=tg_name,
        Protocol='HTTP',
        VpcId='vpc-7d587715',
        Port=80,
        TargetType='instance'
    )['TargetGroups']

    # get the target
    tg_arn = response[0]['TargetGroupArn']

    # input the running ec2 instance you want to attach to the target group
    response = tg.register_targets(
        TargetGroupArn=tg_arn,
        Targets=[
            {
                'Id': 'i-03ca4a7e6a3795f8d',
            },
            {
                'Id': 'i-0b6fc4b7f2a0ac2cf',
            },
        ],
    )
    return tg_arn


create_loadbalancer("Loadbalancer1", 'application')
