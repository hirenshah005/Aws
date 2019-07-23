import boto3
import json


def get_system_manager_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    association_details = []
    document_details = []
    command_details = []
    for region in regions:
        client = boto3.client('ssm', region_name=region)
        response = client.list_associations()['Associations']
        association_names = []

        for res in response:
            association_names.append(res['Name'])

        for name in association_names:
            response = client.describe_association(
                Name=name
            )['AssociationDescription']
            req_info = []
            req_info.append(response)
            association_details.append(req_info)

        response = client.list_documents()['DocumentIdentifiers']
        doc_names = []

        for res in response:
            doc_names.append(res['Name'])

        for name in doc_names:
            response = client.describe_document(
                Name=name
            )['Document']
            req_info = []
            req_info.append(response)
            document_details.append(req_info)

        response = client.list_commands()['Commands']

        for res in response:
            req_info = []
            req_info.append(res)
            command_details.append(req_info)

    dict_associations = {"Associations": association_details}
    dict_documents = {"Documents": document_details}
    dict_commands = {"Commands": command_details}

    json_associations = json.dumps(dict_associations, indent=4, default=str)
    json_documents = json.dumps(dict_documents, indent=4, default=str)
    json_commands = json.dumps(dict_commands, indent=4, default=str)

    print(json_associations)
    print(json_documents)
    print(json_commands)


get_system_manager_info()
