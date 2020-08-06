import requests
import base64

import os
import base64

image_file = "images/sample_receipt.jpg"

encoded_string = ""
with open(image_file, "rb") as f:
    encoded_string = base64.b64encode(f.read()).decode("utf-8")

url = "https://vecxv9wz88.execute-api.ap-southeast-1.amazonaws.com/v1/ocr-detection"
data = {"name": "sample_receipt.jpg", "file": encoded_string, "provider": "ntuc"}

response = requests.post(url, json=data)
json_response = response.json()

print(json_response)
