import os

import boto3

REGION_NAME = os.environ["REGION_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]


def create_presigned_post(
    object_name, bucket_name=BUCKET_NAME, fields=None, conditions=None, expiration=3600
):

    s3_client = boto3.client(
        "s3",
        region_name=REGION_NAME,
    )
    response = s3_client.generate_presigned_post(
        bucket_name,
        object_name,
        Fields=fields,
        Conditions=conditions,
        ExpiresIn=expiration,
    )
    return response
