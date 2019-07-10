import boto3


def vpc_info(region):
    conn = boto3.resource('ec2', region_name=region)
    ec2 = boto3.client('ec2', region_name=region)
    vpc_dict = ec2.describe_vpcs()
    vpc_list = vpc_dict['Vpcs']
    vpc_req_info = vpc_list[0]
    vpc_req_options = ['CidrBlock', 'VpcId']
    vpc_info = []

    for k, v in vpc_req_info.items():
        for i in range(0, len(vpc_req_options)):
            if k == vpc_req_options[i]:
                vpc_info.append(vpc_req_info[k])

    instance_ids = list(conn.instances.filter(InstanceIds=[]))
    req_id = list(conn.instances.filter(Filters=[{'Name': 'instance-id', 'Values': ['i-0fca6b6238e831f79']}]))
    subnet_id = req_id[0].subnet

    for i in range(0, len(vpc_req_options)):
        print('{0} : {1}'.format(vpc_req_options[i], vpc_info[i]))
    print(subnet_id)


vpc_info("ap-south-1")
