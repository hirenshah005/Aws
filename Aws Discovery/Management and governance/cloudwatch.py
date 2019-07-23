import boto3
import datetime


def req_id(req_id):
    """
    Function to get req ids of cloudwatch
    """
    conn = boto3.resource('ec2', region_name='ap-south-1')
    instances = []
    # Refine to get only ids
    for i in conn.instances.all():
        instances.append(i.id)
    for i in range(0, len(instances)):
        if instances[i] == req_id:
            return instances[i]


def cloudwatch_info(id):
    """
    Function that describes the cloudwatch info
    """
    client = boto3.client('cloudwatch', region_name='ap-south-1')
    # get required stats from metrics
    temp_1 = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': id,
            },
        ],
        StartTime=datetime.datetime(2019, 5, 10),
        EndTime=datetime.datetime(2019, 5, 15),
        Statistics=['Average'],
        Period=86400,
        Unit='Percent'
    )
    # print the datapoints
    for cpu in temp_1['Datapoints']:
        if 'Average' in cpu:
            print(cpu['Average'])


return_id = req_id('i-0338183406391b69f')
cloudwatch_info(return_id)
