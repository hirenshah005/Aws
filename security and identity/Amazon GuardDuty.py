# import boto3
# import json
#
#
# def get_guardduty_info():
#     conn = boto3.client('ec2')
#     regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
#
#     for region in regions:
#         if region == 'ap-east-1':
#             continue
#
#         client = boto3.client('guardduty', region_name=region)
#         response =
