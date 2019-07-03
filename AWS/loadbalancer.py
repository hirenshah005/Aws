import boto3


def get_load_balancers(region):
    """
    Function to get all load balancer names
    """
    client = boto3.client('elbv2', region_name=region)
    resource = client.describe_load_balancers()
    resource = resource['LoadBalancers']
    load_balancer_names = []
    # appending only names of load balancer
    for i in range(len(resource)):
        temp = resource[i]
        load_balancer_names.append(temp['LoadBalancerName'])
    return load_balancer_names


def load_balancer_info(id, region):
    """
    Function to list load balancer info
    """
    client = boto3.client('elbv2', region_name=region)
    resource = client.describe_load_balancers(Names=[id])
    resource = resource['LoadBalancers'][0]
    # refining for req keys
    req_params = ['LoadBalancerArn', 'DNSName', 'CreatedTime', 'VpcId', 'Type', 'AvailabilityZones', 'SecurityGroups']
    lb_info = []
    for k, v in resource.items():
        for i in range(len(req_params)):
            if k == req_params[i]:
                # append only req resource
                lb_info.append(resource[k])

    # select target group of load balancer
    target_grp = client.describe_target_groups(
        LoadBalancerArn=lb_info[0]
    )
    # refine to get specfic info using keys
    target_grp = target_grp['TargetGroups'][0]
    req_params_trg = ['TargetGroupName', 'Protocol', 'Port', 'HealthCheckPort']
    trgt_params = []
    for k, v in target_grp.items():
        for i in range(len(req_params_trg)):
            if k == req_params_trg[i]:
                trgt_params.append(target_grp[k])

    for i in range(len(req_params)):
        print("{0} : {1}".format(req_params[i], lb_info[i]))
    for i in range(len(req_params_trg)):
        print("{0} : {1}".format(req_params_trg[i], trgt_params[i]))


value = get_load_balancers('ap-south-1')
print(value)
load_balancer_info(value[0], 'ap-south-1')
