import boto3


def create_iam(user_name, passwd):
    iam = boto3.client('iam', region_name='ap-south-1')

    usernames = []
    response = iam.list_users()['Users']

    for res in response:
        usernames.append(res['UserName'])

    for uname in usernames:
        if uname == user_name:
            print("User Exists")
            exit(0)

    iam.create_user(
        UserName=user_name,
    )

    iam.create_login_profile(
        UserName=user_name,
        Password=passwd,
        PasswordResetRequired=True
    )

    response = iam.create_access_key(
        UserName=user_name
    )
    print(response)

    iam.attach_user_policy(
        UserName=user_name,
        PolicyArn='arn:aws:iam::aws:policy/AmazonEC2FullAccess'
    )


create_iam('sampleuser5', '12345678')
