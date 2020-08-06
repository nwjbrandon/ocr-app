from aws_services import analyze_object, store_object
from fair_price_receipt import FairPriceReceipt


def get_params(event):
    if "provider" not in event:
        return {"status_code": 422, "error": "The field provider is missing"}
    if "name" not in event:
        return {"status_code": 422, "error": "The field name is missing"}
    if "file" not in event:
        return {"status_code": 422, "error": "The field file is missing"}
    return event["provider"], event["name"], event["file"]


def lambda_handler(event, context):
    provider, name, image = get_params(event=event)

    try:
        object_name = store_object(name=name, image=image)
    except:
        return {"status_code": 404, "error": "There is error storing the image in S3"}

    try:
        data = analyze_object(object_name=object_name)
    except:
        return {"status_code": 404, "error": "There is error analyzing the image in S3"}

    if provider == "ntuc":
        receipt = FairPriceReceipt(data=data)
        results = receipt.run()
    else:
        return {"status_code": 422, "error": "The provider is not supported"}

    return {"status_code": 200, "results": results, "file_name": object_name}
