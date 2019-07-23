import boto3
import json

rds_instances_id = []


def get_ids(region):
    # Aws connect
    rds = boto3.client('rds', region_name=region)
    # Select DB-instance specified by user
    db_instance_info = rds.describe_db_instances()
    db_instances_count = db_instance_info['DBInstances']
    # Get all the instances in the specified DB
    for i in range(0, len(db_instances_count)):
        db_instance_names_temp = db_instance_info['DBInstances'][i]
        rds_instances_id.append(db_instance_names_temp['DBInstanceIdentifier'])

    return rds_instances_id


def rds_info(db_id):
    # connect to aws
    rds = boto3.client('rds', region_name="ap-south-1")
    # describe the instances
    full_desc = rds.describe_db_instances(
        # DBInstanceIdentifier=rds_instances_id[i],
        Filters=[
            {
                'Name': 'db-instance-id',
                'Values': [db_id]

            }
        ]
    )
    # Converting the obtained dict into array
    full_desc_values = full_desc['DBInstances']
    required_values_list = full_desc_values[0]

    # Required keys
    req_keys = ['DBInstanceIdentifier', 'DBInstanceClass', 'Engine', 'MasterUsername', 'Endpoint', 'AllocatedStorage',
                'DBSecurityGroups', 'DBSubnetGroup', 'EngineVersion',
                'DBInstanceArn']
    req_values = []

    # loop to get the required key values
    for k, v in required_values_list.items():
        for i in range(0, len(req_keys)):
            if k == req_keys[i]:
                if k == 'DBSubnetGroup':
                    temp = required_values_list[k]
                    req_values.append(temp['VpcId'])
                else:
                    req_values.append(required_values_list[k])

    # Display the values
    for i in range(0, len(req_values)):
        print("{0} : {1}".format(req_keys[i], req_values[i]))
    print("Security groups : {}".format(rds.describe_db_security_groups()))


def get_all_rds_info():
    conn = boto3.client('ec2')
    # List all regions
    req_info = []
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    for region in regions:
        conn = boto3.client('rds', region_name=region)
        full_desc = conn.describe_db_instances()
        full_desc_values = full_desc['DBInstances']

        for i in range(len(full_desc_values)):
            required_values_list = full_desc_values[i]
            # Required keys
            req_keys = ['DBInstanceIdentifier', 'DBInstanceClass', 'Engine', 'MasterUsername', 'Endpoint',
                        'AllocatedStorage',
                        'DBSecurityGroups', 'DBSubnetGroup', 'EngineVersion',
                        'DBInstanceArn']
            req_values = []

            # loop to get the required key values
            for k, v in required_values_list.items():
                for i in range(0, len(req_keys)):
                    if k == req_keys[i]:
                        if k == 'DBSubnetGroup':
                            temp = required_values_list[k]
                            req_values.append(temp['VpcId'])
                        else:
                            req_values.append(required_values_list[k])
            req_info.append(req_values)

    list_rds = []
    req_keys = ['DBInstanceIdentifier', 'DBInstanceClass', 'Engine', 'MasterUsername', 'Endpoint',
                'AllocatedStorage',
                'DBSecurityGroups', 'DBSubnetGroup', 'EngineVersion',
                'DBInstanceArn']
    for i in req_info:
        dictionary = dict(zip(req_keys,i))
        list_rds.append(dictionary)

    final_dict = {"Rds":list_rds}
    json_final = json.dumps(final_dict, indent=4)
    print(json_final)


# Func call
# req_ids = get_ids("ap-south-1")
# rds_info(req_ids[0])
get_all_rds_info()
