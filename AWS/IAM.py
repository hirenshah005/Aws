import boto3


def iam_names(region):
    client = boto3.client('iam', region_name=region)
    response = client.list_users()
    response = response['Users']
    iam_name = []
    for i in range(len(response)):
        temp = response[i]
        iam_name.append(temp['UserName'])
    return iam_name


def iam_details(region, iam_req):
    client = boto3.client('iam', region_name=region)
    response = client.get_user(
        UserName=iam_req
    )
    response = response['User']

    print("User Details:")
    print()
    for k, v in response.items():
        if k == 'Path':
            continue
        else:
            print("{0} : {1}".format(k, v))
    print()

    print("policy_details:")
    print()
    response = client.list_policies(
        OnlyAttached=True
    )
    response = response['Policies']
    for i in range(len(response)):
        temp = response[i]
        for k, v in temp.items():
            if k == 'PolicyName' or k == 'PolicyId' or k == 'Arn' or k == 'CreateDate':
                print("{0} : {1}".format(k, v))
        print()
    print()

    response = client.list_groups_for_user(
        UserName=iam_req
    )
    response = response['Groups'][0]

    print("Group Details:")
    print()
    for k, v in response.items():
        if k == 'Path':
            continue
        else:
            print("{0} : {1}".format(k, v))


value = iam_names('ap-south-1')
iam_details('ap-south-1', value[0])
