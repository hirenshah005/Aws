import boto3


def create_key():
    ec2 = boto3.resource('ec2', region_name='ap-south-1')

    # create a file to store the key locally
    outfile = open('ec2-keypair.pem', 'w')

    # call the boto ec2 function to create a key pair
    key_pair = ec2.create_key_pair(KeyName='ec2-keypair')

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    print(KeyPairOut)
    outfile.write(KeyPairOut)


def create_instance():
    ec2 = boto3.resource('ec2', region_name='ap-south-1')

    # create a new EC2 instance
    instances = ec2.create_instances(
        ImageId='ami-0d2692b6acea72ee6',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName='ec2-keypair'
    )


create_instance()
