import base64
import os
import uuid

import boto3

ACCESS_KEY = os.environ["ACCESS_KEY"]
SECRET_KEY = os.environ["SECRET_KEY"]
REGION_NAME = os.environ["REGION_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]


def store_object(name, image):
    parts = name.split(".")
    object_name = f"{parts[0]}_{str(uuid.uuid4())}.{parts[1]}"
    image = image[image.find(",") + 1 :]
    dec = base64.b64decode(image + "===")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION_NAME,
    )
    s3_client.put_object(Bucket=BUCKET_NAME, Key=object_name, Body=dec)
    return object_name


def analyze_object(object_name):
    client = boto3.client(
        "textract",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION_NAME,
    )
    results = client.detect_document_text(
        Document={"S3Object": {"Bucket": BUCKET_NAME, "Name": object_name}}
    )
    return results
