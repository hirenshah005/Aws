# import boto3
# import json
#
#
# def get_cognito_info():
#     conn = boto3.client('ec2')
#     regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
#
#     for region in regions:
#         if region == 'ap-east-1' or region == 'eu-north-1' or region == 'sa-east-1' or region == 'us-west-1' or region == 'eu-west-3':
#             continue
#
#
