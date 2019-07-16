import boto3
import json


def get_step_function_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    machine_info = []
    execution_info = []
    for region in regions:
        client = boto3.client('stepfunctions', region_name=region)
        response = client.list_state_machines()['stateMachines']
        machine_names = []
        for res in response:
            machine_names.append(res['stateMachineArn'])

        for arn in machine_names:
            response = client.describe_state_machine(
                stateMachineArn=arn
            )
            req_info = []
            req_info.append(response)
            machine_info.append(req_info)

        exec_names =[]
        for arn in machine_names:
            response = client.list_executions(
                stateMachineArn=arn
            )['executions']
            exec_names.append(response['executionArn'])

        for arn in exec_names:
            response = client.describe_execution(
                executionArn=arn
            )
            req_info = []
            req_info.append(response)
            execution_info.append(req_info)

    dict_machine_info = {"State Machines": machine_info}
    dict_exection_info = {"Execution": execution_info}

    json_machine = json.dumps(dict_machine_info, indent=4, default=str)
    json_execution = json.dumps(dict_exection_info, indent=4, default=str)

    print(json_machine)
    print(json_execution)


get_step_function_info()