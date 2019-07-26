import boto3


def create_loadbalancer(lb_name, vpc, protocol):
    """
    A fucntion to create load balancer
    """
    client = boto3.client('elb', region_name='ap-south-1')
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
        LoadBalancerName=lb_name,
        Listeners=[
            {
                'Protocol': protocol,
                'LoadBalancerPort': 80,
                'InstancePort': 80,

            },
        ],
        Subnets=subnets
    )

    response = client.register_instances_with_load_balancer(
        LoadBalancerName=lb_name,
        Instances=[
            {
                'InstanceId': 'i-074c56ce8b59e515f'
            },
            {
                'InstanceId': 'i-08eb4e570fa4cdf6b'
            }
        ]
    )


create_loadbalancer("Loadbalancer1", 'vpc-7d587715', "HTTP")
