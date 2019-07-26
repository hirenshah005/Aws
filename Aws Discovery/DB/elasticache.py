import boto3
import json


def get_elasticache_info():
    """
    A function to get elasticache cache clusters info
    """
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    elaticache = []
    for region in regions:
        conn = boto3.client('elasticache', region_name=region)
        # describe the clusters
        response = conn.describe_cache_clusters()['CacheClusters']
        # the requried keys for the cluster
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
                    # append only the required keys
                    if k == req_keys[i]:
                        req_info.append(res[k])
            elaticache.append(req_info)

    elsticache_list = []
    # the required keys for elasticache
    req_keys = ['CacheClusterId', 'ClientDownloadLandingPage', 'CacheNodeType', 'Engine', 'EngineVersion',
                'CacheClusterStatus', 'NumCacheNodes', 'PreferredAvailabilityZone', 'CacheClusterCreateTime',
                'PreferredMaintenanceWindow', 'CacheSecurityGroups', 'CacheSubnetGroupName',
                'AutoMinorVersionUpgrade', 'SecurityGroups', 'SnapshotRetentionLimit', 'AuthTokenEnabled',
                'TransitEncryptionEnabled', 'AtRestEncryptionEnabled']

    # convert to dictionary
    for i in elaticache:
        dict_elasti = dict(zip(req_keys, i))
        elsticache_list.append(dict_elasti)

    # final dict
    final_dict = {"ElastiCache": elsticache_list}
    # convert to json
    json_elastic = json.dumps(final_dict, indent=4, default=str)
    print(json_elastic)


get_elasticache_info()
