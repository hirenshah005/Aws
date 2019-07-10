import boto3


def cost_info():
    client = boto3.client('ce')
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': '2019-01-01',
            'End': '2019-05-01'
        },
        Granularity='MONTHLY',
        Metrics=['AmortizedCost']

    )
    print(response)


cost_info()
