import boto3
import json


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
    # refine and print application info
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

    # Refine and print environment info
    print("Environment Info")
    print()
    response = conn.describe_environments(
        ApplicationName=req_app
    )
    response = response['Environments']
    req_info = []

    # select only req key info
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

    # additional environment info
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

    # instance info
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


def get_all_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    app_info = []
    env_info = []
    inst_info = []
    for region in regions:
        conn = boto3.client('elasticbeanstalk', region_name=region)
        # selecting the req applications
        response = conn.describe_applications()
        # refine and print application info
        response = response['Applications']
        for j in response:
            req_keys = ['ApplicationArn', 'ApplicationName', 'DateCreated', 'Versions']
            req_info = []
            for k in j.keys():
                for i in range(len(req_keys)):
                    if k == req_keys[i]:
                        req_info.append(j[k])
            app_info.append(req_info)

        response = conn.describe_environments()
        response = response['Environments']
        env_names = []

        for j in response:
            env_names.append(j['EnvironmentName'])

        for j in response:
            req_info = []
            # select only req key inf
            req_keys = ['EnvironmentName', 'EnvironmentId', 'ApplicationName', 'SolutionStackName', 'PlatformArn',
                        'EndpointURL', 'DateCreated', 'Status', 'Health', 'HealthStatus', 'Tier', 'EnvironmentArn']
            for k in j.keys():
                for l in range(len(req_keys)):
                    if k == req_keys[l]:
                        req_info.append(j[k])

            # additional environment info
            for h in env_names:
                response = conn.describe_environment_resources(
                    EnvironmentName=h
                )
                response = response['EnvironmentResources']
                req_info.append(response['AutoScalingGroups'])
                req_info.append(response['Instances'])
                req_info.append(response['LaunchConfigurations'])
            env_info.append(req_info)

        # instance info

        req_info = []
        for z in env_names:
            response = conn.describe_instances_health(
                EnvironmentName=z,
                AttributeNames=[
                    'HealthStatus', 'System', 'AvailabilityZone', 'InstanceType'
                ]
            )
            response = response['InstanceHealthList']
            for j in response:
                for k, v in j.items():
                    req_info.append(j[k])
                inst_info.append(req_info)
 
    req_keys_app = ['ApplicationArn', 'ApplicationName', 'DateCreated', 'Versions']
    req_keys_env = ['EnvironmentName', 'EnvironmentId', 'ApplicationName', 'SolutionStackName', 'PlatformArn',
                    'EndpointURL', 'DateCreated', 'Status', 'Health', 'HealthStatus', 'Tier', 'EnvironmentArn',
                    'AutoscalingGroups', 'Instances', 'LaunchConfigurations']
    req_keys_inst = ['HealthStatus', 'System', 'AvailabilityZone', 'InstanceType']
    app_list = []
    env_list = []
    inst_list= []

    for i in app_info:
        dict_app = dict(zip(req_keys_app,i))
        app_list.append(dict_app)

    for i in env_info:
        dict_env = dict(zip(req_keys_env,i))
        env_list.append(dict_env)

    for i in inst_info:
        dict_inst = dict(zip(req_keys_inst,i))
        inst_list.append(dict_inst)

    final_app_dict = {"Application Info": app_list}
    final_env_dict = {"Environement Info": env_list}
    final_inst_dict = {"Instances Info": inst_list}

    json_app = json.dumps(final_app_dict,indent=4,default=str)
    json_env = json.dumps(final_env_dict, indent=4, default=str)
    json_inst = json.dumps(final_inst_dict, indent=4, default=str)

    print(json_app)
    print(json_env)
    print(json_inst)


# values = get_info('ap-south-1')
# get_application_info('ap-south-1', values[0])
get_all_info()
