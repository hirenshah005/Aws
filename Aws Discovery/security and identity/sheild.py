import boto3
import json


def get_sheild_info():
    """
    A fucntion that gives shield's attacks and protections
    """
    conn = boto3.client('shield')
    attack_info = []
    protection_info = []
    subscription_info = []
    attack_ids = []
    # get all attack ids
    response = conn.list_attacks()['AttackSummaries']

    for res in response:
        attack_ids.append(res['AttackId'])

    # describe each atacck
    for ids in attack_ids:
        response = conn.describe_attack(
            AttackId=ids
        )
        req_info = []
        req_info.append(response)
        # append each attack as separate list
        attack_info.append(req_info)

    # get protections info
    response = conn.list_protections()['Protections']

    for res in response:
        req_info = []
        req_info.append(res)
        protection_info.append(req_info)

    # get subscriptions info
    response = conn.describe_subscription()['Subscription']

    for res in response:
        req_info = []
        req_info.append(res)
        subscription_info.append(req_info)

    # convert attack protection and subscription list into dictionary
    attack_dict = {"Attack Info": attack_info}
    protection_dict = {"Protection": protection_info}
    subscription_dict = {"Subscriptions": subscription_info}

    # convert dictionaries into json
    attack_json = json.dumps(attack_dict, indent=4, default=str)
    protection_json = json.dumps(protection_dict, indent=4, default=str)
    subscription_json = json.dumps(subscription_dict, indent=4, default=str)

    print(attack_json)
    print(protection_json)
    print(subscription_json)


get_sheild_info()
