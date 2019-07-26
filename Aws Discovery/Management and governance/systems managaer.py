import boto3
import json


def get_system_manager_info():
    """
    A fucntion that gives the associations and documents details
    """
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    association_details = []
    document_details = []
    command_details = []
    for region in regions:
        client = boto3.client('ssm', region_name=region)
        # list associations to get association names
        response = client.list_associations()['Associations']
        association_names = []

        # appending the names
        for res in response:
            association_names.append(res['Name'])

        # describing each association
        for name in association_names:
            response = client.describe_association(
                Name=name
            )['AssociationDescription']
            req_info = []
            req_info.append(response)
            # appending each assocaition as seperate lists
            association_details.append(req_info)

        # list documents to get document names
        response = client.list_documents()['DocumentIdentifiers']
        doc_names = []

        for res in response:
            doc_names.append(res['Name'])

        # describe each document
        for name in doc_names:
            response = client.describe_document(
                Name=name
            )['Document']
            req_info = []
            req_info.append(response)
            # append each document as seperate list
            document_details.append(req_info)

        # get command info
        response = client.list_commands()['Commands']

        for res in response:
            req_info = []
            req_info.append(res)
            command_details.append(req_info)

    # convert docuents and commands into dictionary
    dict_associations = {"Associations": association_details}
    dict_documents = {"Documents": document_details}
    dict_commands = {"Commands": command_details}

    # convert dictionary into json
    json_associations = json.dumps(dict_associations, indent=4, default=str)
    json_documents = json.dumps(dict_documents, indent=4, default=str)
    json_commands = json.dumps(dict_commands, indent=4, default=str)

    print(json_associations)
    print(json_documents)
    print(json_commands)


get_system_manager_info()
