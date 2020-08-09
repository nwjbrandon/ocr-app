try:
    from aws_services import analyze_object, store_object, store_results
    from receipt_utils import ReceiptContentExtractor
    from validator_utils import get_params
except ImportError:
    from src.aws_services import analyze_object, store_object, store_results
    from src.receipt_utils import ReceiptContentExtractor
    from src.validator_utils import get_params


def run_ocr(event):
    name, image = get_params(event=event)

    try:
        object_name = store_object(name=name, image=image)
    except:
        return {
            "status_code": 404,
            "error": "There is an error storing the image in S3",
            "file_name": name,
        }

    try:
        data = analyze_object(object_name=object_name)
    except:
        return {
            "status_code": 404,
            "error": "There is an error analyzing the image in S3",
            "file_name": object_name,
        }

    try:
        extractor = ReceiptContentExtractor(data=data)
        results = extractor.run()
    except:
        return {
            "status_code": 404,
            "error": "There is an error extracting content in the receipt",
            "file_name": object_name,
        }

    try:
        store_results(name=object_name, data={"results": results, "data": data})
    except:
        return {
            "status_code": 404,
            "error": "There is an error storing logs in S3",
            "file_name": object_name,
        }

    return {"status_code": 200, "results": results, "file_name": object_name}
