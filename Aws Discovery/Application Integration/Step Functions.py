import boto3
import json


def get_step_function_info():
    """
    Function to get statemachine and execution info
    """
    # usinf ec2 to describe regions
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    machine_info = []
    execution_info = []
    # looping through all regions
    for region in regions:
        client = boto3.client('stepfunctions', region_name=region)
        # list the state machines
        response = client.list_state_machines()['stateMachines']
        machine_names = []
        for res in response:
            machine_names.append(res['stateMachineArn'])
        # describing each state machines
        for arn in machine_names:
            response = client.describe_state_machine(
                stateMachineArn=arn
            )
            req_info = []
            req_info.append(response)
            # seperate lists for seperating info
            machine_info.append(req_info)

        exec_names = []
        # getting the execution arns
        for arn in machine_names:
            response = client.list_executions(
                stateMachineArn=arn
            )['executions']
            exec_names.append(response['executionArn'])

        # describing each execution
        for arn in exec_names:
            response = client.describe_execution(
                executionArn=arn
            )
            req_info = []
            req_info.append(response)
            # seperate lists for seperating info
            execution_info.append(req_info)

    # Converting list to dictionaries for json
    dict_machine_info = {"State Machines": machine_info}
    dict_exection_info = {"Execution": execution_info}

    # converting dictionary to json
    json_machine = json.dumps(dict_machine_info, indent=4, default=str)
    json_execution = json.dumps(dict_exection_info, indent=4, default=str)

    print(json_machine)
    print(json_execution)


get_step_function_info()
