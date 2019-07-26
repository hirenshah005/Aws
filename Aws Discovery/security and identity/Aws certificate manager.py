import boto3
import json


def get_certificate_info():
    """
    A funtion that gives info about all the certificates
    """
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    certificates_info = []

    for region in regions:
        client = boto3.client('acm', region_name=region)
        # list all certificates to get the certificate arn
        response = client.list_certificates()['CertificateSummaryList']
        certificates_names = []

        for res in response:
            certificates_names.append(res['CertificateArn'])

        # get each cerificate info
        for arn in certificates_names:
            response = client.get_certificate(
                CertificateArn=arn
            )
            req_info = []
            req_info.append(response)
            certificates_info.append(req_info)
    # convert cerificate list into dictionary
    certificates_dict = {"Certificates": certificates_info}
    # convert dictionary to json
    certificates_json = json.dumps(certificates_dict, indent=4, default=str)

    print(certificates_json)


get_certificate_info()
