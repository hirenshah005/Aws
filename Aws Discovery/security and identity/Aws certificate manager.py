import boto3
import json


def get_certificate_info():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    certificates_info = []

    for region in regions:
        client = boto3.client('acm', region_name=region)
        response = client.list_certificates()['CertificateSummaryList']
        certificates_names = []
        for res in response:
            certificates_names.append(res['CertificateArn'])

        for arn in certificates_names:
            response = client.get_certificate(
                CertificateArn=arn
            )
            req_info = []
            req_info.append(response)
            certificates_info.append(req_info)

    certificates_dict = {"Certificates": certificates_info}
    certificates_json = json.dumps(certificates_dict, indent=4, default=str)

    print(certificates_json)


get_certificate_info()
