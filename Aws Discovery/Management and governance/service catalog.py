import boto3
import json


def get_service_catalog_details():
    """
    A fucntion that gives the portfolio and and record information
    """
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    portfolio_info = []
    record_info = []
    for region in regions:
        if region == 'ap-east-1':
            continue
        client = boto3.client('servicecatalog')
        # list all the portfolios to get its ids
        response = client.list_portfolios()['PortfolioDetails']
        portfoilio_ids = []
        for res in response:
            portfoilio_ids.append(res['Id'])

        # get each portfolio info
        for ids in portfoilio_ids:
            response = client.describe_portfolio(
                Id=ids
            )
            for res in response:
                req_info = []
                req_info.append(res)
                # append each portfolio as a separate list
                portfolio_info.append(req_info)

        # list all records to get record id
        response = client.list_record_history()['RecordDetails']
        record_ids = []
        for res in response:
            record_ids.append(res['RecordId'])

        # describe each record
        for ids in record_ids:
            response = client.describe_record(
                Id=ids
            )

            req_info = []
            req_info.append(response)
            # append each record as a seperate list
            record_info.append(req_info)

    # convert the portfolio and record lists into dicitonaries
    dict_portfolio = {"Portfolio": portfolio_info}
    dict_records = {"Records": record_info}

    # convert the dictionaries to json
    json_portfolio = json.dumps(dict_portfolio, indent=4, default=str)
    json_records = json.dumps(dict_records, indent=4, default=str)

    print(json_portfolio)
    print(json_records)


get_service_catalog_details()
