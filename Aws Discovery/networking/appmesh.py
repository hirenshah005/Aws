import boto3
import json


def get_aws_mesh_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    appmeshes = []
    route_info = []

    for region in regions:
        if region == 'ap-east-1' or region == 'eu-west-3' or region == 'eu-north-1' or region == 'sa-east-1':
            continue

        conn = boto3.client('appmesh', region_name=region)
        response = conn.list_meshes()['meshes']

        appmesh_names = []
        for res in response:
            appmesh_names.append(res['meshName'])

        for name in appmesh_names:
            response = conn.describe_mesh(
                meshName=name
            )
            req_info = []
            for res in response:
                req_info.append(res)
            appmeshes.append(req_info)

    mesh_dict = {"Mesh": appmeshes}
    mesh_json = json.dumps(mesh_dict, indent=4, default=str)

    print(mesh_json)


get_aws_mesh_info()
