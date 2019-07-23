import boto3


def create_loadbalancer(lb_name, app_type):
    client = boto3.client('elbv2', region_name='ap-south-1')
    conn = boto3.client('ec2', region_name='ap-south-1')
    response = conn.describe_subnets()['Subnets']
    subnets = []

    for res in response:
        subnets.append(res['SubnetId'])

    response = client.create_load_balancer(
        Name=lb_name,
        Subnets=subnets,
        Type=app_type
    )['LoadBalancers']

    lb_arn = response[0]['LoadBalancerArn']

    tg_arn = create_target_group('tg1')

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
    tg = boto3.client('elbv2', region_name='ap-south-1')
    response = tg.create_target_group(
        Name=tg_name,
        Protocol='HTTP',
        VpcId='vpc-7d587715',
        Port=80,
        TargetType='instance'
    )['TargetGroups']

    tg_arn = response[0]['TargetGroupArn']

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
