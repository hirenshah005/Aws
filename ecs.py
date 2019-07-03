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

    response = conn.describe_services(
        cluster=req_info[0]
    )
    print(response)


value = get_info('ap-south-1')
get_cluster_info('ap-south-1', value[0])
