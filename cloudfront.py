import boto3


def get_cloudfront_ids():
    """
    Function to retrive the cloudfront names
    """
    # Connect to cloufront
    client = boto3.client('cloudfront')
    info = client.list_distributions()
    # selecting only required keys
    info = info['DistributionList']
    info = info['Items']
    ids = []
    # refining to get only names
    for i in range(0, len(info)):
        temp = info[i]
        for k, v in temp.items():
            if k == 'Id':
                ids.append(temp[k])
    return ids


def get_cloudfront_info(Id):
    """
    Fucntion to descibe the required id
    """
    client = boto3.client('cloudfront')
    # Select the required id
    response = client.get_distribution(
        Id=Id
    )
    # selecting only req keys
    req_ids = response['Distribution']
    req_ids_dist = ['Id', 'ARN', 'DomainName', 'DistributionConfig']
    req_info = []
    for k, v in req_ids.items():
        for i in range(0, len(req_ids_dist)):
            # appending only req key values
            if k == req_ids_dist[i]:
                req_info.append(req_ids[k])

    for i in range(0, len(req_info)):
        # Breaking down key for finer info
        if req_ids_dist[i] == 'DistributionConfig':
            temp = req_info[i]
            req_params = temp['Origins']
            req_params = req_params['Items']
            group_ids = []
            group_domains = []
            for j in range(0, len(req_params)):
                temp = req_params[j]
                group_ids.append(temp['Id'])
                group_domains.append(temp['DomainName'])
            print("Group ids : {}".format(group_ids))
            print("Group domains : {}".format(group_domains))

        else:
            print("{0} : {1}".format(req_ids_dist[i], req_info[i]))


value = get_cloudfront_ids()
get_cloudfront_info(value[0])
