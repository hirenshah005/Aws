import boto3
import json


def get_sns_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    sms_attrib = []
    subscriptions_attrib = []
    topic_attrib = []

    for region in regions:
        client = boto3.client('sns', region_name=region)
        response = client.get_sms_attributes()['attributes']

        for res in response:
            req_info = []
            req_info.append(res)
            sms_attrib.append(req_info)

        subscriptions_arns = []
        response = client.list_subscriptions()['Subscriptions']
        for res in response:
            subscriptions_arns.append(res['SubscriptionArn'])

        for arn in subscriptions_arns:
            response = client.get_subscription_attributes(
                SubscriptionArn=arn
            )
            req_info = []
            req_info.append(response)
            subscriptions_attrib.append(req_info)

        list_names = []
        response = client.response = client.list_topics()['Topics']
        for res in response:
            list_names.append(res)

        for arn in list_names:
            response = client.get_topic_attributes(
                TopicArn=arn
            )
            req_info = []
            req_info.append(response)
            topic_attrib.append(req_info)


get_sns_info()
