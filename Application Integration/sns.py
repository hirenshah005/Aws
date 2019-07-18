import boto3
import json


def get_sns_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    sms_attrib = []
    subscriptions_attrib = []
    topic_attrib = []

    for region in regions:
        if region == 'us-west-2':
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
        else:
            continue

    sms_dict = {"SMS": sms_attrib}
    subscription_dict = {"Subscriptions": subscriptions_attrib}
    topics_dict = {"Topics": topic_attrib}

    json_dict = json.dumps(sms_dict, indent=4, default=str)
    json_subscription = json.dumps(subscription_dict, indent=4, default=str)
    json_topic = json.dumps(topics_dict, indent=4, default=str)

    print(json_dict)
    print(json_subscription)
    print(json_topic)


get_sns_info()
