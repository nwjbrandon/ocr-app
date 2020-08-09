import argparse
import json
import os

from dotenv import load_dotenv

from src.aws_services import analyze_object, store_results
from src.ocr_utils import ReceiptContentExtractor

load_dotenv(dotenv_path=".env")

ACCESS_KEY = os.environ["ACCESS_KEY"]
SECRET_KEY = os.environ["SECRET_KEY"]
REGION_NAME = os.environ["REGION_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]


def main(object_name):
    data = analyze_object(
        object_name,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        bucket_name=BUCKET_NAME,
        region_name=REGION_NAME,
    )
    extractor = ReceiptContentExtractor(data=data)
    results = extractor.run()

    store_results(
        name=object_name,
        data=results,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        bucket_name=BUCKET_NAME,
        region_name=REGION_NAME,
    )

    results = json.dumps(results, indent=2)

    print(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-on", "--object_name", help="Object name in S3", required=True)
    args = parser.parse_args()
    object_name = args.object_name

    main(object_name=object_name)
