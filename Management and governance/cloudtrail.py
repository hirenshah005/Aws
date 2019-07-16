import boto3
import json
from datetime import datetime
import time


def get_cloudtrail_info(start_time, end_time, max_result):
    conn = boto3.client('ec2')
    regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
    trail_info = []
    event_info = []
    # for region in regions:
    client = boto3.client('cloudtrail', region_name='ap-south-1')
    response = client.describe_trails()['trailList']

    for res in response:
        req_info = []
        req_info.append(res)
        trail_info.append(req_info)

    time_start = time.strptime(start_time, '%d-%m-%Y')
    time_end = time.strptime(end_time, '%d-%m-%Y')

    time_start = datetime(time_start.tm_year, time_start.tm_mon, time_start.tm_mday)
    time_end = datetime(time_end.tm_year, time_end.tm_mon, time_end.tm_mday)

    response = client.lookup_events(
        StartTime=time_start,
        EndTime=time_end,
        MaxResults=max_result,
    )['Events']

    for res in response:
        req_info = []
        req_info.append(res)
        event_info.append(req_info)

    dict_trail = {"Trails": trail_info}
    dict_events = {"Events": event_info}

    json_trail = json.dumps(dict_trail, indent=4, default=str)
    json_events = json.dumps(dict_events, indent=4, default=str)

    print(json_trail)
    print(json_events)


get_cloudtrail_info("14-07-2019", "15-07-2019", 10)
