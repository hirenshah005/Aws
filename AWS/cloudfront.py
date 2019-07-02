import boto3


def get_cloudfront_ids():
    client = boto3.client('cloudfront')
    info = client.list_distributions()
    info = info['DistributionList']
    info = info['Items']
    ids = []
    for i in range(0, len(info)):
        temp = info[i]
        for k, v in temp.items():
            if k == 'Id':
                ids.append(temp[k])
    # print(ids)
    return ids


def get_cloudfront_info(Id):
    client = boto3.client('cloudfront')
    response = client.get_distribution(
        Id=Id
    )
    req_ids = response['Distribution']
    req_ids_dist = ['Id', 'ARN', 'DomainName', 'DistributionConfig']
    req_info = []
    for k, v in req_ids.items():
        for i in range(0, len(req_ids_dist)):
            if k == req_ids_dist[i]:
                req_info.append(req_ids[k])

    for i in range(0, len(req_info)):

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
