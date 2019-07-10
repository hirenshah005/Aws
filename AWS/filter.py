import boto3
import json

# sample progtam on how to use filters
ec2 = boto3.client('ec2',region_name="ap-south-1")
desc = ec2.describe_instances(Filters=[
        {
            'Name': 'tag:Name',
            # 'Values': ['Sample']
        }
    ]
)
print(desc)