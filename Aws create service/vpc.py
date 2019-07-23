import boto3


def create_vpc(cidr_block, public_subnets, private_subnets):
    ec2 = boto3.resource('ec2', region_name='ap-south-1')
    conn = boto3.client('ec2', region_name='ap-south-1')

    respone = conn.describe_vpcs()['Vpcs']
    cidr_blocks = []

    for res in respone:
        cidr_blocks.append(res['CidrBlock'])

    for block in cidr_blocks:
        if block == cidr_block:
            print("CIDR Exist")
            exit(0)

    vpc = ec2.create_vpc(CidrBlock=cidr_block)
    vpc.create_tags(Tags=[{"Key": "Name", "Value": "default_vpc"}])
    vpc.wait_until_available()
    print(vpc.id)

    ig = ec2.create_internet_gateway()
    vpc.attach_internet_gateway(InternetGatewayId=ig.id)
    print(ig.id)

    route_table = vpc.create_route_table()
    route_table.create_tags(Tags=[{"Key": "Name", "Value": "Route Table 1"}])
    route = route_table.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=ig.id
    )
    print(route_table.id)
    cidr_template = cidr_block.split('.')
    cidr_template[3] = cidr_template[3].split('/')
    print(cidr_template)
    count = 0
    for i in range(public_subnets):
        subnet = ec2.create_subnet(
            CidrBlock='{0}.{1}.{2}.{3}/24'.format(cidr_template[0], cidr_template[1], count, cidr_template[3][0]),
            VpcId=vpc.id)
        subnet.create_tags(Tags=[{"Key": "Name", "Value": "Public-Subnet-{}".format(i)}])
        count += 1

        route_table.associate_with_subnet(
            SubnetId=subnet.id
        )

    for i in range(private_subnets):
        subnet = ec2.create_subnet(
            CidrBlock='{0}.{1}.{2}.{3}/24'.format(cidr_template[0], cidr_template[1], count, cidr_template[3][0]),
            VpcId=vpc.id)
        subnet.create_tags(Tags=[{"Key": "Name", "Value": "Private-Subnet-{}".format(i)}])
        count += 1


create_vpc('10.0.0.0/16', 1, 1)
