import boto3
import json


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
    print(load_balancer_names)
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


def get_full_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    load_balancer = []
    target_grps = []
    for region in regions:
        client = boto3.client('elbv2', region_name=region)
        resource = client.describe_load_balancers()
        resource = resource['LoadBalancers']

        for z in resource:
            # refining for req keys
            req_params = ['LoadBalancerArn', 'DNSName', 'CreatedTime', 'LoadBalancerName', 'VpcId', 'Type',
                          'AvailabilityZones',
                          'SecurityGroups']
            lb_info = []
            for k, v in z.items():
                for i in range(len(req_params)):
                    if k == req_params[i]:
                        # append only req resource
                        lb_info.append(z[k])
            load_balancer.append(lb_info)

            # select target group of load balancer
        target_grp = client.describe_target_groups()
        # refine to get specfic info using keys
        target_grp = target_grp['TargetGroups']
        for z in target_grp:
            req_params_trg = ['TargetGroupName', 'Protocol', 'Port', 'HealthCheckPort']
            trgt_params = []
            for k, v in z.items():
                for i in range(len(req_params_trg)):
                    if k == req_params_trg[i]:
                        trgt_params.append(z[k])
            target_grps.append(trgt_params)
    load_balancer_list = []
    target_groups_list = []
    req_params_lb = ['LoadBalancerArn', 'DNSName', 'CreatedTime', 'LoadBalancerName', 'VpcId', 'Type',
                     'AvailabilityZones',
                     'SecurityGroups']
    req_params_trg = ['TargetGroupName', 'Protocol', 'Port', 'HealthCheckPort']

    for i in load_balancer:
        dict_lb = dict(zip(req_params_lb, i))
        load_balancer_list.append(dict_lb)

    for i in target_grps:
        dict_tg = dict(zip(req_params_trg, i))
        target_groups_list.append(dict_tg)

    final_load_dict = {"Load Balancers": load_balancer_list}
    final_trg_dict = {"Target Groups": target_groups_list}

    json_lb = json.dumps(final_load_dict, indent=4, default=str)
    json_trg = json.dumps(final_trg_dict, indent=4, default=str)

    print(json_lb)
    print(json_trg)


# value = get_load_balancers('ap-south-1')
# load_balancer_info(value[0], 'ap-south-1')
get_full_info()
