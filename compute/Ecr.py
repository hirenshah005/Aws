import boto3
import json


def get_info(region):
    """
    Function to get all ecr names
    """
    conn = boto3.client('ecr', region_name=region)
    response = conn.describe_repositories()
    # filter only req keys
    response = response['repositories']
    rep_names = []
    for i in range(len(response)):
        temp = response[i]
        # appending only names
        rep_names.append(temp['repositoryName'])
    return rep_names


def get_rep_info(region, req_rep_name):
    """
    Function that lists the details of the repo and it contents
    """
    conn = boto3.client('ecr', region_name=region)
    # get ony req repo
    response = conn.describe_repositories(
        repositoryNames=[req_rep_name]
    )
    # Take only info of required keys
    response = response['repositories'][0]
    req_keys = ['repositoryArn', 'registryId', 'repositoryName', 'repositoryUri', 'createdAt']
    req_info = []
    for k in response.keys():
        for i in range(len(req_keys)):
            if k == req_keys[i]:
                # append only req info
                req_info.append(response[k])

    print("Repo info")
    print()
    for i in range(len(req_info)):
        print('{0} : {1}'.format(req_keys[i], req_info[i]))
    print()

    # select only req image
    response = conn.describe_images(
        registryId=req_info[1],
        repositoryName=req_info[2],
    )

    # Filter only req keys
    response = response['imageDetails']
    print("Image Details")
    print()
    for i in range(len(response)):
        req_info = []
        temp = response[i]
        req_keys = ['repositoryName', 'imageDigest', 'imageTags', 'imageSizeInBytes', 'imagePushedAt']
        for k in temp.keys():
            for l in range(len(req_keys)):
                if k == req_keys[l]:
                    req_info.append(temp[k])

        for m in range(len(req_info)):
            print('{0} : {1}'.format(req_keys[m], req_info[m]))
        print()


def get_full_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    repo_info = []
    img_info = []
    for region in regions:
        conn = boto3.client('ecr', region_name=region)
        response = conn.describe_repositories()
        # Take only info of required keys
        response = response['repositories']
        for j in response:
            req_keys = ['repositoryArn', 'registryId', 'repositoryName', 'repositoryUri', 'createdAt']
            req_info = []
            for k in j.keys():
                for i in range(len(req_keys)):
                    if k == req_keys[i]:
                        # append only req info
                        req_info.append(j[k])
            repo_info.append(req_info)

        rep_names = []
        for i in range(len(response)):
            temp = response[i]
            # appending only names
            rep_names.append(temp['repositoryName'])

        for i in rep_names:
            response = conn.describe_images(
                repositoryName=i
            )
            # Filter only req keys
            response = response['imageDetails']
            for z in range(len(response)):
                req_info = []
                temp = response[z]
                req_keys = ['repositoryName', 'imageDigest', 'imageTags', 'imageSizeInBytes', 'imagePushedAt']
                for k in temp.keys():
                    for l in range(len(req_keys)):
                        if k == req_keys[l]:
                            req_info.append(temp[k])
                img_info.append(req_info)

    repo_list = []
    img_list = []
    req_keys_repo = ['repositoryArn', 'registryId', 'repositoryName', 'repositoryUri', 'createdAt']
    req_keys_imgs = ['repositoryName', 'imageDigest', 'imageTags', 'imageSizeInBytes', 'imagePushedAt']

    for i in repo_info:
        dict_repo = dict(zip(req_keys_repo, i))
        repo_list.append(dict_repo)

    for i in img_info:
        dict_img = dict(zip(req_keys_imgs, i))
        img_list.append(dict_img)

    final_repo = {"Repostory Info": repo_list}
    final_img = {"Image List": img_list}

    json_repo = json.dumps(final_repo,indent=4,default=str)
    json_img = json.dumps(final_img, indent=4, default=str)

    print(json_repo)
    print(json_img)


# value = get_info('ap-south-1')
# get_rep_info('ap-south-1', value[0])
get_full_info()
