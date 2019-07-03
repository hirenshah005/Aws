import boto3


def get_info(region):
    """
    Function to get Names of all the Application Names and return it
    """
    # Establish connection
    conn = boto3.client('elasticbeanstalk', region_name=region)
    response = conn.describe_applications()
    # select only required key
    response = response['Applications']
    application_names = []
    # Filter all the responses to get only name
    for i in range(len(response)):
        temp = response[i]
        temp = temp['ApplicationName']
        application_names.append(temp)

    return application_names


def get_application_info(region, req_app):
    """
       Function that gets all the required info of the app
    """
    conn = boto3.client('elasticbeanstalk', region_name=region)
    # selecting the req applications
    response = conn.describe_applications(
        ApplicationNames=[req_app]
    )
    response = response['Applications'][0]
    req_keys = ['ApplicationArn', 'ApplicationName', 'DateCreated', 'Versions']
    req_info = []
    for k in response.keys():
        for i in range(len(req_keys)):
            if k == req_keys[i]:
                req_info.append(response[k])

    print("Application Info")
    print()
    for i in range(len(req_info)):
        print("{0} : {1}".format(req_keys[i], req_info[i]))
    print()

    print("Environment Info")
    print()
    response = conn.describe_environments(
        ApplicationName=req_app
    )
    response = response['Environments']
    req_info = []

    for i in range(len(response)):
        temp = response[i]
        req_keys = ['EnvironmentName', 'EnvironmentId', 'ApplicationName', 'SolutionStackName', 'PlatformArn',
                    'EndpointURL', 'DateCreated', 'Status', 'Health', 'HealthStatus', 'Tier', 'EnvironmentArn']

        for k in temp.keys():
            for l in range(len(req_keys)):
                if k == req_keys[l]:
                    req_info.append(temp[k])

        for j in range(len(req_keys)):
            print("{0} : {1}".format(req_keys[j], req_info[j]))

    response = conn.describe_environment_resources(
        EnvironmentName=req_info[0]

    )
    response = response['EnvironmentResources']
    print('AutoScalingGroups:{}'.format(response['AutoScalingGroups']))
    print('Instances: {}'.format(response['Instances']))
    print('LaunchConfigurations'.format(response['LaunchConfigurations']))
    print()

    print("Instance_info")
    print()

    response = conn.describe_instances_health(
        EnvironmentName=req_info[0],
        EnvironmentId=req_info[1],
        AttributeNames=[
            'HealthStatus', 'System', 'AvailabilityZone', 'InstanceType'
        ],

    )
    response = response['InstanceHealthList']
    for i in range(len(response)):
        temp = response[i]
        for k, v in temp.items():
            print("{0} : {1}".format(k, v))


values = get_info('ap-south-1')
get_application_info('ap-south-1', values[0])
