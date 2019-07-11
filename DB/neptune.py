import boto3
import json


def get_neptune_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    neptune_cluster = []
    neptune_instances = []
    req_keys_cluster = []
    req_keys_instances = []
    conn = boto3.client('neptune', region_name='ap-south-1')
    response = conn.describe_db_clusters()['DBClusters'][0]

    for k in response.keys():
        req_keys_cluster.append(k)

    response = conn.describe_db_instances()['DBInstances'][0]
    for k in response.keys():
        req_keys_instances.append(k)

    for region in regions:

        if region == 'us-west-1' or region == 'ap-east-1' or region == 'ca-central-1' or region == 'eu-west-3' or region == 'sa-east-1':
            continue
        conn = boto3.client('neptune', region_name=region)
        response = conn.describe_db_clusters()['DBClusters']
        for res in response:
            req_info = []

            if 'KmsKeyId' in res:
                continue
            for k in res.keys():
                req_info.append(res[k])
            neptune_cluster.append(req_info)

        response = conn.describe_db_instances()['DBInstances']
        for res in response:
            req_info = []
            if 'KmsKeyId' in res:
                continue
            for k in res.keys():
                req_info.append(res[k])
            neptune_instances.append(req_info)

    neptune_cluster_list = []
    neptune_instance_list = []
    print(req_keys_instances)
    print(req_keys_cluster)

    for i in neptune_cluster:
        dict_cluster = dict(zip(req_keys_cluster, i))
        neptune_cluster_list.append(dict_cluster)

    for i in neptune_instances:
        dict_instances = dict(zip(req_keys_instances, i))
        neptune_instance_list.append(dict_instances)

    final_cluster = {"Clusters": neptune_cluster_list}
    final_instances = {"Instances": neptune_instance_list}

    json_cluster = json.dumps(final_cluster, indent=4, default=str)
    json_instance = json.dumps(final_instances, indent=4, default=str)

    print(json_cluster)
    print(json_instance)


get_neptune_info()
