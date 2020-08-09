import argparse
import base64
import json

import requests


def main(image_file):

    encoded_string = ""
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode("utf-8")

    url = "https://vecxv9wz88.execute-api.ap-southeast-1.amazonaws.com/v1/ocr-detection"
    data = {"name": "sample_receipt.jpg", "file": encoded_string, "provider": "ntuc"}

    response = requests.post(url, json=data)
    json_response = response.json()
    json_response = json.dumps(json_response, indent=2)

    print(json_response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-if", "--image_file", help="File path to image", required=True)
    args = parser.parse_args()
    image_file = args.image_file

    main(image_file=image_file)
