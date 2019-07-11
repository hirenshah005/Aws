import boto3
import json


def get_elasticache_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    elaticache = []
    for region in regions:
        conn = boto3.client('elasticache', region_name=region)
        response = conn.describe_cache_clusters()['CacheClusters']
        req_keys = ['CacheClusterId', 'ClientDownloadLandingPage', 'CacheNodeType', 'Engine', 'EngineVersion',
                    'CacheClusterStatus', 'NumCacheNodes', 'PreferredAvailabilityZone', 'CacheClusterCreateTime',
                    'PreferredMaintenanceWindow', 'CacheSecurityGroups', 'CacheSubnetGroupName',
                    'AutoMinorVersionUpgrade', 'SecurityGroups', 'SnapshotRetentionLimit', 'AuthTokenEnabled',
                    'TransitEncryptionEnabled', 'AtRestEncryptionEnabled']
        print(response)
        for res in response:
            req_info = []
            for k in res.keys():
                for i in range(len(req_keys)):
                    if k == req_keys[i]:
                        req_info.append(res[k])
            elaticache.append(req_info)

    elsticache_list = []
    req_keys = ['CacheClusterId', 'ClientDownloadLandingPage', 'CacheNodeType', 'Engine', 'EngineVersion',
                'CacheClusterStatus', 'NumCacheNodes', 'PreferredAvailabilityZone', 'CacheClusterCreateTime',
                'PreferredMaintenanceWindow', 'CacheSecurityGroups', 'CacheSubnetGroupName',
                'AutoMinorVersionUpgrade', 'SecurityGroups', 'SnapshotRetentionLimit', 'AuthTokenEnabled',
                'TransitEncryptionEnabled', 'AtRestEncryptionEnabled']

    for i in elaticache:
        dict_elasti = dict(zip(req_keys, i))
        elsticache_list.append(dict_elasti)

    final_dict = {"ElastiCache": elsticache_list}
    json_elastic = json.dumps(final_dict, indent=4, default=str)
    print(json_elastic)


get_elasticache_info()
