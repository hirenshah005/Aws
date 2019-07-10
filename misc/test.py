import boto3
import json

conn = boto3.client('ec2',region_name='ap-south-1')
response = conn.describe_instances()
json = json.dumps(response,default=str)
print(json[1])