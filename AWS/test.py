import boto3

client = boto3.client('iam', region_name='ap-south-1')
response = client.list_policies(
        OnlyAttached=True
    )
print(response)