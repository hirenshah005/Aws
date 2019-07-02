import boto3
import json

ec2 = boto3.client('ec2',region_name="ap-south-1")
desc = ec2.describe_instances(Filters=[
        {
            'Name': 'tag:Name',
            'Values': ['Sample']
        }
    ]
)