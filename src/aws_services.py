import base64
import json
import os
import uuid

import boto3

try:
    ACCESS_KEY = os.environ["ACCESS_KEY"]
    SECRET_KEY = os.environ["SECRET_KEY"]
    REGION_NAME = os.environ["REGION_NAME"]
    BUCKET_NAME = os.environ["BUCKET_NAME"]
except KeyError:
    ACCESS_KEY = None
    SECRET_KEY = None
    REGION_NAME = None
    BUCKET_NAME = None


def store_object(
    name,
    image,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    bucket_name=BUCKET_NAME,
    region_name=REGION_NAME,
):
    parts = name.split(".")
    object_name = f"{parts[0]}_{str(uuid.uuid4())}.{parts[1]}"
    image = image[image.find(",") + 1 :]
    dec = base64.b64decode(image + "===")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region_name,
    )
    s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=dec)
    return object_name


def store_results(
    name,
    data,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    bucket_name=BUCKET_NAME,
    region_name=REGION_NAME,
):
    parts = name.split(".")
    object_name = f"{parts[0]}.json"
    dec = json.dumps(data, indent=2)
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region_name,
    )
    s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=dec)


def analyze_object(
    object_name,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    bucket_name=BUCKET_NAME,
    region_name=REGION_NAME,
):
    client = boto3.client(
        "textract",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region_name,
    )
    results = client.detect_document_text(
        Document={"S3Object": {"Bucket": bucket_name, "Name": object_name}}
    )
    return results
