import boto3
from datetime import datetime


def create_s3_bucket(bucket_name):
    """
    create s3 bucket
    """
    conn = boto3.client('s3')
    response = conn.create_bucket(
        Bucket=bucket_name,
    )
    # put objects to bucket
    response = conn.put_object(
        Bucket=bucket_name,
        Key='generateClassifier.py',
        Body='sample'
    )
    # set lifecycle
    response = conn.put_bucket_lifecycle(
        Bucket='string',
        LifecycleConfiguration={
            'Rules': [
                {
                    'Expiration': {
                        'Date': datetime(2019, 10, 1),
                        'Days': 10,
                        'ExpiredObjectDeleteMarker': True
                    },
                    'Prefix': 'abc',
                    'Status': 'Enabled',
                    'Transition': {
                        'Date': datetime(2019, 11, 1),
                        'Days': 10,
                        'StorageClass': 'GLACIER'
                    },
                    'NoncurrentVersionTransition': {
                        'NoncurrentDays': 10,
                        'StorageClass': 'GLACIER'
                    },
                    'NoncurrentVersionExpiration': {
                        'NoncurrentDays': 10
                    },
                    'AbortIncompleteMultipartUpload': {
                        'DaysAfterInitiation': 10
                    }
                },
            ]
        }
    )

create_s3_bucket('126e1f3dv')
