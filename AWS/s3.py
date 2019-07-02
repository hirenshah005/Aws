import boto3


def get_bucket_list(region):
    client = boto3.client('s3', region_name=region)
    bucket_list_full_info = client.list_buckets()
    bucket_list_dict = bucket_list_full_info['Buckets']
    bucket_list = []
    for i in bucket_list_dict:
        bucket_list.append(i["Name"])
    print(bucket_list)
    return bucket_list[0]


def bucket_object_info(region, bucket_req):
    client = boto3.client('s3', region_name=region)
    bucket_object = client.list_objects(
        Bucket=bucket_req
    )
    bucket_contents_dict = bucket_object['Contents']
    bucket_contents = []
    for i in bucket_contents_dict:
        bucket_contents.append(i["Key"])
    print(bucket_contents)
    return bucket_contents[0]


def object_info(region, obj_info, bucket_req):
    client = boto3.client('s3', region_name=region)
    bucket_object = client.list_objects(
        Bucket=bucket_req
    )
    req_obj_info = []
    bucket_contents_dict = bucket_object['Contents']
    for i in bucket_contents_dict:
        for k, v in i.items():
            if i[k] == obj_info:
                req_obj_info.append(i)
                
    req_obj_info = req_obj_info[0]
    object_info = []
    obj_info_req = ['Key', 'LastModified', 'ETag', 'Size', 'Owner']

    for k, v in req_obj_info.items():
        for i in range(0, len(obj_info_req)):
            if k == obj_info_req[i]:
                object_info.append(req_obj_info[k])

    for i in range(0, len(obj_info_req)):
        print("{0} : {1}".format(obj_info_req[i], object_info[i]))


bucket_list = get_bucket_list("ap-south-1")
object_value = bucket_object_info("ap-south-1", bucket_list)
object_info("ap-south-1", object_value, bucket_list)
