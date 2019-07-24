import boto3


def create_efs(token_name):
    """
    A function to create efs file system
    """
    conn = boto3.client('efs', region_name='ap-south-1')
    # create the file system
    response = conn.create_file_system(
        CreationToken=token_name,
        PerformanceMode='generalPurpose',
        Encrypted=False,
        ThroughputMode='bursting',
    )
    # get the created file system info
    print(response)


create_efs('tok1')
