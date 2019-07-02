import boto3
import datetime


def req_id(req_id):
    conn = boto3.resource('ec2', region_name='ap-south-1')
    instances = []
    for i in conn.instances.all():
        instances.append(i.id)
    for i in range(0, len(instances)):
        if instances[i] == req_id:
            return instances[i]




def cloudwatch_info(id):
    client = boto3.client('cloudwatch', region_name='ap-south-1')
    temp = client.list_metrics()
    #print(temp)
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
        # ExtendedStatistics = ['0.0'],
        Unit='Percent'
    )
    #print(temp_1)
    for cpu in temp_1['Datapoints']:
        if 'Average' in cpu:
            print(cpu['Average'])


return_id = req_id('i-0338183406391b69f')
cloudwatch_info(return_id)
