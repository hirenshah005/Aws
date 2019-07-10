import boto3


def get_route_details(region):
    client = boto3.client('route53', region_name=region)
    response = client.list_hosted_zones()
    response = response['HostedZones']
    ids = []
    for i in range(len(response)):
        temp = response[i]
        ids.append(temp['Id'])
    return ids


def get_route_dets(region, req_id):
    client = boto3.client('route53', region_name=region)
    response = client.get_hosted_zone(
        Id=req_id
    )
    response = response['HostedZone']
    print("ID : {}".format(response['Id']))
    print("Name : {}".format(response['Name']))


value = get_route_details('ap-south-1')
get_route_dets('ap-south-1', value[0])
