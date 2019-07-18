# import boto3
# import json
#
# def get_swf_info():
#     conn = boto3.client('ec2')
#     regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
#
#     for region in regions:
#