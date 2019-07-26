import boto3
import json


# def get_route_details(region):
#     client = boto3.client('route53', region_name=region)
#     response = client.list_hosted_zones()
#     response = response['HostedZones']
#     ids = []
#     for i in range(len(response)):
#         temp = response[i]
#         ids.append(temp['Id'])
#     return ids
#
#
# def get_route_dets(region, req_id):
#     client = boto3.client('route53', region_name=region)
#     response = client.get_hosted_zone(
#         Id=req_id
#     )
#     response = response['HostedZone']
#     print("ID : {}".format(response['Id']))
#     print("Name : {}".format(response['Name']))


def get_all_route_details():
    """
    A fucntion that gives route 53 hosted zones informarion
    """
    conn = boto3.client('route53')
    # get all hosted zones ids
    response = conn.list_hosted_zones()['HostedZones']
    route_ids = []
    route_info = []
    for res in response:
        route_ids.append(res['Id'])

    # get info of each hosted zone
    for ids in route_ids:
        response = conn.get_hosted_zone(
            Id=ids
        )['HostedZone']
        route_info.append(response)

    # convert zone list to dictionary
    final_dict = {"Route 53": route_info}
    # covert dictionart to json
    json_final = json.dumps(final_dict, indent=4, default=str)
    print(json_final)


# value = get_route_details('ap-south-1')
# get_route_dets('ap-south-1', value[0])
get_all_route_details()
