import boto3


def get_running_instances():
    conn = boto3.resource('ec2', region_name="ap-south-1")
    instances = conn.instances.filter()
    for instance in instances:
        if instance.state["Name"] == "running":
            print(instance.id, instance.instance_type, "ap-south-1")


def get_all_instance_desc():
    conn = boto3.client('ec2', region_name="ap-south-1")
    response = conn.describe_instances()
    response = response['Reservations']
    # print(response[0])
    # print(response[1])
    for i in range(len(response)):
        temp = response[i]
        temp = temp['Instances'][0]

        req_keys = ['ImageId', 'InstanceId', 'InstanceType', 'LaunchTime', 'Placement', 'NetworkInterfaces']
        req_info = []
        for k in temp.keys():
            for i in range(len(req_keys)):
                if k == req_keys[i]:
                    req_info.append(temp[k])

        for i in range(len(req_info)):
            if req_keys[i] == "NetworkInterfaces":
                temp = req_info[i]
                if  temp == []:
                    print("Instace terminated")
                else:
                    temp = temp[0]
                    temp = temp['Association']
                    elastic_check = temp['IpOwnerId']
                    if elastic_check == 'amazon':
                        elastic_check = False
                    else:
                        elastic_check = True
                    print("Elastic Ip: {}".format(elastic_check))
            else:
                print("{0} : {1}".format(req_keys[i],req_info[i]))
        print()
        req_info = []



def get_specfic_instances(inst_id):
    conn = boto3.resource('ec2', region_name="ap-south-1")
    ec2 = boto3.client('ec2', region_name="ap-south-1")
    desc = ec2.describe_instances(Filters=[
        {
            'Name': 'instance-id',
            'Values': [inst_id]
        }
    ]
    )
    req_info = ['Reservations', 'Placement', 'PublicIpAddress', 'SubnetId', 'SubnetId']
    req_info_list = []
    for k, v in desc.items():
        for i in range(0, len(req_info)):
            if k == req_info[i]:
                req_info_list.append(desc[k])
    req_info_list = req_info_list[0][0]
    req_info_list_refined = []
    more_filters = ['Instances', 'OwnerId']
    for k in req_info_list.keys():
        for i in range(0, len(more_filters)):
            if k == more_filters[i]:
                req_info_list_refined.append(req_info_list[k])
    req_info_list_refined = req_info_list_refined[0][0]
    # req_info_list_refined = req_info_list_refined['Instances']
    req_info_proper = []
    more_filters = ['ImageId', 'InstanceId', 'InstanceType', 'Placement', 'PublicIpAddress', 'SubnetId', 'VpcId']
    for k, v in req_info_list_refined.items():
        for i in range(0, len(more_filters)):
            if k == more_filters[i]:
                req_info_proper.append(req_info_list_refined[k])

    for i in range(0, len(req_info_proper)):
        print("{0} : {1}".format(more_filters[i], req_info_proper[i]))


print("----------------------------------------------------")
print("get_running_instances:")
print()
# get_running_instances()
print("----------------------------------------------------")
print("get_instance_desc:")
print()
get_all_instance_desc()
print("----------------------------------------------------")
print("get_instance__full_desc:")
# get_specfic_instances('i-0cb4324b8c1a4334e')
