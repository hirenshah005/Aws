import boto3
import json


def get_efs_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    efs_info = []
    for region in regions:
        if region == 'ap-east-1' or region == 'sa-east-1' or region == 'eu-north-1':
            continue
        conn = boto3.client('efs', region_name=region)
        response = conn.describe_file_systems()['FileSystems']
        for res in response:
            req_info = []
            for k in res.keys():
                if k == 'Tags':
                    continue
                req_info.append(res[k])

            mount_trg_ids = []
            subnets = []
            ips = []
            net_ids = []
            response = conn.describe_mount_targets(
                        FileSystemId=res['FileSystemId']
                    )['MountTargets']
            for i in response:
                mount_trg_ids.append(i['MountTargetId'])
                subnets.append(i['SubnetId'])
                ips.append(i['IpAddress'])
                net_ids.append(i['NetworkInterfaceId'])
            req_info.append(mount_trg_ids)
            req_info.append(subnets)
            req_info.append(ips)
            req_info.append(net_ids)
            efs_info.append(req_info)

    efs_list = []
    req_keys = ['OwnerId', 'CreationToken', 'FileSystemId', 'CreationTime', 'LifeCycleState', 'NumberOfMountTargets',
                'SizeInBytes', 'PerformanceMode', 'Encrypted', 'ThroughputMode', 'MountTargetId',
                'SubnetId', 'IpAddress', 'NetworkInterfaceId']
    for i in efs_info:
        dict_efs = dict(zip(req_keys, i))
        efs_list.append(dict_efs)

    final_dict = {"EFS": efs_list}
    json_efs = json.dumps(final_dict, indent=4, default=str)

    print(json_efs)


get_efs_info()
