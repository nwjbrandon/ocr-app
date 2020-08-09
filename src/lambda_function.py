from ocr_utils import run_ocr


def lambda_handler(event, context):
    return run_ocr(event=event)
