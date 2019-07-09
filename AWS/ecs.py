import boto3


def get_info(region):
    """
    function to get ecs names
    """
    conn = boto3.client('ecs', region_name=region)
    response = conn.describe_clusters()
    response = response['clusters']
    names = []
    # filter only names
    for i in range(len(response)):
        temp = response[i]
        names.append(temp['clusterName'])
    return names


def get_cluster_info(region, cluster_req):
    """
    Funtion to desc required ecs info
    """
    conn = boto3.client('ecs', region_name=region)
    response = conn.describe_clusters(
        clusters=[cluster_req]

    )
    # filtering out only the required info
    response = response['clusters'][0]
    req_keys = ['clusterArn', 'clusterName', 'status', 'registeredContainerInstancesCount', 'runningTasksCount',
                'pendingTasksCount', 'activeServicesCount']
    req_info = []
    for k in response.keys():
        for i in range(len(req_keys)):
            if k == req_keys[i]:
                req_info.append(response[k])

    print('Cluster info')
    print()
    for i in range(len(req_info)):
        print('{0} : {1}'.format(req_keys[i], req_info[i]))

    # listing the service
    response = conn.list_services(
        cluster=req_info[0]
    )
    #  getting the service arns to use in describe func
    response = response['serviceArns']
    service_arns = []
    for i in range(len(response)):
        temp = response[i]
        service_arns.append(temp)

    # describing the arns

    response = conn.describe_services(
        cluster=req_info[0],
        services=service_arns
    )

    response = response['services']
    req_keys = ['serviceArn', 'serviceName', 'clusterArn', 'loadBalancers', 'status', 'taskDefinition', 'deployments',
                'networkConfiguration']

    print("service info")
    print()
    req_info = []
    req_info_list = []
    for i in range(len(response)):
        temp = response[i]
        for k in temp.keys():
            for l in range(len(req_keys)):
                if k == req_keys[l]:
                    req_info.append(temp[k])
        req_info_list.append(req_info)

    for j in range(len(req_info_list)):
        temp = req_info_list[j]
        for k in range(len(req_keys)):
            print('{0} : {1}'.format(req_keys[k], temp[k]))
        print()

    # task lists
    task_arns = []
    response = conn.list_tasks(
        cluster=cluster_req
    )
    response = response['taskArns']
    for i in range(len(response)):
        task_arns.append(response[i])

    # describing tasks:

    response = conn.describe_tasks(
        tasks=task_arns
    )

    response = response['tasks']
    keys_req = ['taskArn', 'clusterArn', 'taskDefinitionArn', 'lastStatus', 'cpu', 'memory',
                'group', 'launchType', 'attachments']
    info = []
    info_list = []

    print("task info")
    print()
    for i in range(len(response)):
        temp = response[i]
        for k in temp.keys():
            for l in range(len(keys_req)):
                if k == keys_req[l]:
                    info.append(temp[k])
        info_list.append(info)
        info = []

    for i in range(len(info_list)):
        for j in range(len(keys_req)):
            if keys_req[j] == 'attachments':
                temp = info_list[i]
                temp = temp[-1]
                temp = temp[0]
                temp = temp['details']
                temp = temp[1]
                del info_list[i][j]
                info_list[i].append(temp['value'])
                ec2 = boto3.client('ec2', region_name=region)
                response = ec2.describe_network_interfaces(
                    NetworkInterfaceIds=[info_list[i][j]]
                )
                ip = response['NetworkInterfaces'][0]
                ip = ip['Association']['PublicIp']
                print("Public Ip: {0}".format(ip))
            else:
                temp = info_list[i]
                print("{0} : {1}".format(keys_req[j], temp[j]))
        print()


def get_all_cluster_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    cluster_info = []
    service_info = []
    task_info = []
    for region in regions:
        conn = boto3.client('ecs', region_name=region)
        response = conn.describe_clusters()
        # filtering out only the required info
        response = response['clusters']
        for z in response:
            req_keys = ['clusterArn', 'clusterName', 'status', 'registeredContainerInstancesCount', 'runningTasksCount',
                        'pendingTasksCount', 'activeServicesCount']
            req_info = []
            for k in z.keys():
                for i in range(len(req_keys)):
                    if k == req_keys[i]:
                        req_info.append(z[k])
            cluster_info.append(req_info)

        # listing the service
        response = conn.list_services(

        )
        #  getting the service arns to use in describe func
        response = response['serviceArns']
        service_arns = []
        for i in range(len(response)):
            temp = response[i]
            service_arns.append(temp)

            # describing the arns

        response = conn.describe_services(
            services= service_arns
        )

        response = response['services']
        req_keys = ['serviceArn', 'serviceName', 'clusterArn', 'loadBalancers', 'status', 'taskDefinition',
                    'deployments',
                    'networkConfiguration']

        for z in response:
            req_info = []
            for k in z.keys():
                for l in range(len(req_keys)):
                    if k == req_keys[l]:
                        req_info.append(z[k])
            service_info.append(req_info)

        # # task lists
        # task_arns = []
        # response = conn.list_tasks(
        #     cluster=cluster_req
        # )
        # response = response['taskArns']
        # for i in range(len(response)):
        #     task_arns.append(response[i])

        # describing tasks:

        response = conn.describe_tasks()

        response = response['tasks']
        keys_req = ['taskArn', 'clusterArn', 'taskDefinitionArn', 'lastStatus', 'cpu', 'memory',
                    'group', 'launchType', 'attachments']
        info = []
        info_list = []

        for z in response:
            for k in z.keys():
                for l in range(len(keys_req)):
                    if k == keys_req[l]:
                        info.append(z[k])
            task_info.append(info)

        for i in range(len(info)):
            for j in range(len(keys_req)):
                if keys_req[j] == 'attachments':
                    temp = info_list[i]
                    temp = temp[-1]
                    temp = temp[0]
                    temp = temp['details']
                    temp = temp[1]
                    del task_info[i]
                    ec2 = boto3.client('ec2', region_name=region)
                    response = ec2.describe_network_interfaces(
                        NetworkInterfaceIds=[info_list[i][j]]
                    )
                    ip = response['NetworkInterfaces'][0]
                    ip = ip['Association']['PublicIp']
                    task_info.append(ip)

    print(cluster_info)
    print(service_info)
    print(task_info)


#
# value = get_info('ap-south-1')
# get_cluster_info('ap-south-1', value[0])
get_all_cluster_info()
