import boto3


def create_efs(token_name):
    conn = boto3.client('ec2', region_name='ap-south-1')
    response = conn.describe_subnets()['Subnets']
    subnets = []

    for res in response:
        subnets.append(res['SubnetId'])

    conn = boto3.client('efs', region_name='ap-south-1')

    response = conn.create_file_system(
        CreationToken=token_name,
        PerformanceMode='generalPurpose',
        Encrypted=False,
        ThroughputMode='bursting',
    )
    print(response)


create_efs('tok1')
