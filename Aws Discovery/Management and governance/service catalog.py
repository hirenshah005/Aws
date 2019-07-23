import boto3
import json


def get_service_catalog_details():
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    portfolio_info = []
    record_info = []
    for region in regions:
        if region == 'ap-east-1':
            continue
        client = boto3.client('servicecatalog')
        response = client.list_portfolios()['PortfolioDetails']
        portfoilio_ids = []
        for res in response:
            portfoilio_ids.append(res['Id'])

        for ids in portfoilio_ids:
            response = client.describe_portfolio(
                Id=ids
            )
            for res in response:
                req_info = []
                req_info.append(res)
                portfolio_info.append(req_info)

        response = client.list_record_history()['RecordDetails']
        record_ids = []
        for res in response:
            record_ids.append(res['RecordId'])

        for ids in record_ids:
            response = client.describe_record(
                Id=ids
            )

            req_info = []
            req_info.append(response)
            record_info.append(req_info)

    dict_portfolio = {"Portfolio": portfolio_info}
    dict_records = {"Records": record_info}

    json_portfolio = json.dumps(dict_portfolio, indent=4, default=str)
    json_records = json.dumps(dict_records, indent=4, default=str)

    print(json_portfolio)
    print(json_records)


get_service_catalog_details()
