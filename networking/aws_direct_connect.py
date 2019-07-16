import boto3
import json


def get_aws_direct_info():
  
    connections = []
    virtual_interfaces = []
    lags = []
    direct_connect_gateways = []

    conn = boto3.client('directconnect')

    response = conn.describe_connections()['connections']

    req_info_connections = []
    for res in response:
        req_info_connections.append(res)
    connections.append(req_info_connections)

    response = conn.describe_virtual_interfaces()['virtualInterfaces']
    req_info_virt_int = []
    for res in response:
        req_info_virt_int.append(res)
    virtual_interfaces.append(req_info_virt_int)

    response = conn.describe_lags()['lags']
    req_info_lags = []
    for res in response:
        req_info_lags.append(res)
    lags.append(req_info_lags)

    response = conn.describe_direct_connect_gateways()['directConnectGateways']
    req_info_gateways = []
    for res in response:
        req_info_gateways.append(res)
    direct_connect_gateways.append(req_info_gateways)

    connections_dict = {"Connections": connections}
    virt_inter_dict = {"Virtual Interfaces": virtual_interfaces}
    lag_dict = {"Lags": lags}
    gateways_dict = {"Direct Connect Gateways": direct_connect_gateways}

    json_connections = json.dumps(connections_dict, indent=4, default=str)
    json_virt_int = json.dumps(virt_inter_dict, indent=4, default=str)
    json_lag = json.dumps(lag_dict, indent=4, default=str)
    json_gateways = json.dumps(gateways_dict, indent=4, default=str)

    print(json_connections)
    print(json_virt_int)
    print(json_lag)
    print(json_gateways)


get_aws_direct_info()