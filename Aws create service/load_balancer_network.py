import boto3


def create_loadbalancer(lb_name, vpc, protocol):
    """
    A fucntion to create load balancer
    """
    client = boto3.client('elbv2', region_name='ap-south-1')
    conn = boto3.client('ec2', region_name='ap-south-1')
    # get subnets to create load balancer (Min=3)
    response = conn.describe_subnets(
        Filters=[
            {
                'Name': 'vpc-id',
                'Values': [
                    vpc
                ]
            }
        ]
    )['Subnets']
    subnets = []

    for res in response:
        subnets.append(res['SubnetId'])

    # create the load balancer

    response = client.create_load_balancer(
        Name=lb_name,
        Subnets=subnets,
        Type='network'
    )['LoadBalancers']

    # get load balancer arn to create the target group
    lb_arn = response[0]['LoadBalancerArn']
    # create the targer group
    tg_arn = create_target_group('tg1', protocol, vpc)

    # create the listener that points to the target group
    response = client.create_listener(
        LoadBalancerArn=lb_arn,
        Protocol=protocol,
        Port=80,
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': tg_arn
            }
        ],
    )


def create_target_group(tg_name, protcol, vpc):
    """
    A function to create the target group
    """
    tg = boto3.client('elbv2', region_name='ap-south-1')
    # create the target groups
    response = tg.create_target_group(
        Name=tg_name,
        Protocol=protcol,
        VpcId=vpc,
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
                'Id': 'i-074c56ce8b59e515f',
            },
            {
                'Id': 'i-08eb4e570fa4cdf6b',
            },
        ],
    )
    return tg_arn


create_loadbalancer("Loadbalancer1", 'vpc-7d587715', "UDP")
