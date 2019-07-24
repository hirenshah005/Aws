import boto3


def create_iam(user_name, passwd):
    """
    A function to create iam user with password and access keys

    assign variable to all boto functions to get the response from it
    """
    iam = boto3.client('iam', region_name='ap-south-1')

    usernames = []
    # get all the usernames
    response = iam.list_users()['Users']

    for res in response:
        usernames.append(res['UserName'])

    # check if username already exists
    for uname in usernames:
        if uname == user_name:
            print("User Exists")
            exit(0)

    # creating user
    iam.create_user(
        UserName=user_name,
    )

    # setting the user name and password
    iam.create_login_profile(
        UserName=user_name,
        Password=passwd,
        PasswordResetRequired=True
    )

    # create the access key for the user
    response = iam.create_access_key(
        UserName=user_name
    )
    print(response)

    # attach the policy for the user to determine the access you want to grant
    iam.attach_user_policy(
        UserName=user_name,
        PolicyArn='arn:aws:iam::aws:policy/AmazonEC2FullAccess'
    )


create_iam('sampleuser5', '12345678')
