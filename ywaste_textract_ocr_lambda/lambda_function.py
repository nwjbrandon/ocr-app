import os

import boto3
from fair_price_receipt import FairPriceReceipt

ACCESS_KEY = os.environ["ACCESS_KEY"]
SECRET_KEY = os.environ["SECRET_KEY"]
REGION_NAME = os.environ["REGION_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]


def run_textract(object_name):
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


def lambda_handler(event, context):
    data = run_textract(object_name=event["file_name"])
    receipt = FairPriceReceipt(data=data)
    results = receipt.run()
    return {"statusCode": 200, "body": results}
