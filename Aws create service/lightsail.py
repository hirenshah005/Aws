import boto3


def create_instance(instance_name, avail_zone, image_name, os_name, bundle):
    conn = boto3.client('lightsail', region_name='ap-south-1')
    response = conn.get_blueprints()['blueprints']
    blueprint_id = []

    for res in response:
        blueprint_id.append(res['blueprintId'])

    if os_name in blueprint_id:
        pass
    else:
        print("Wrong Id")
        exit(0)

    bundle_ids = []
    response = conn.get_bundles()['bundles']

    for res in response:
        bundle_ids.append(res['bundleId'])

    if bundle in bundle_ids:
        pass
    else:
        print("Wrong bundle")
        exit(0)

    response = conn.create_instances(
        instanceNames=[instance_name],
        availabilityZone=avail_zone,
        customImageName=image_name,
        blueprintId=os_name,
        bundleId=bundle
    )

    print(response)


create_instance('instance1', 'ap-south-1a', 'ubuntu1', 'ubuntu_18_04', 'nano_2_1')
