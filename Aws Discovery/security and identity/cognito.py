import boto3
import json


def get_cognito_info():
    """
    A function that gives cognito user pools information
    """
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    user_pool_info = []
    user_info = []

    for region in regions:
        if region == 'ap-east-1' or region == 'eu-north-1' or region == 'sa-east-1' or region == 'us-west-1' or region == 'eu-west-3':
            continue
        conn = boto3.client('cognito-idp', region_name=region)
        user_pool_ids = []

        # list the user pools to get the user pool id
        response = conn.list_user_pools(
            MaxResults=10
        )['UserPools']

        for res in response:
            user_pool_ids.append(res['Id'])

        # describe each user pool
        for ids in user_pool_ids:
            response = conn.describe_user_pool(
                UserPoolId=ids
            )['UserPool']
            req_info = []
            req_info.append(response)
            # append each user pool as a seperate list
            user_pool_info.append(req_info)

            # get user information
            response = conn.list_users(
                UserPoolId=ids
            )['Users']
            req_info = []
            req_info.append(response)
            user_info.append(req_info)

    # convert user pool and user lists into dictionaries
    dict_user_pool = {"User pools": user_pool_info}
    dicts_users = {"Users": user_info}

    # convert dictionaries into json
    user_pool_json = json.dumps(dict_user_pool, indent=4, default=str)
    user_json = json.dumps(dicts_users, indent=4, default=str)

    print(user_pool_json)
    print(user_json)


get_cognito_info()
