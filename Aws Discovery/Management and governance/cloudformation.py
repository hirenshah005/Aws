import boto3
import json


def get_clouformation_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    stacks_info = []
    resource_info = []
    stack_instances = []

    for region in regions:
        client = boto3.client('cloudformation', region_name=region)
        response = client.describe_stacks()['Stacks']

        stack_names = []
        for res in response:
            req_info = []
            stack_names.append(res['StackName'])
            req_info.append(res)
            stacks_info.append(req_info)

        for names in stack_names:
            response = client.describe_stack_resources(
                StackName=names
            )
            req_info = []
            req_info.append(response)
            resource_info.append(req_info)

        stack_set_id = []
        stack_region = []

        for name in stack_names:
            response = client.list_stack_instances(
                StackSetName=name
            )['Summaries']
            stack_set_id.append(response['StackSetId'])
            stack_region.append(response['Region'])

        for i in range(len(stack_names)):
            response = client.describe_stack_instance(
                StackSetName=stack_names[i],
                StackInstanceAccount=stack_set_id[i],
                StackInstanceRegion=stack_region[i]
            )
            req_info = []
            req_info.append(response)
            stack_instances.append(req_info)

    stacks_info_dict = {"Stack Info": stacks_info}
    stacks_resources_dict = {"Resources": resource_info}
    stacks_instances = {"Instances": stack_instances}

    info_json = json.dumps(stacks_info_dict, indent=4, default=str)
    resource_json = json.dumps(stacks_resources_dict, indent=4, default=str)
    instances_json = json.dumps(stacks_instances, indent=4, default=str)

    print(info_json)
    print(resource_json)
    print(instances_json)


get_clouformation_info()
