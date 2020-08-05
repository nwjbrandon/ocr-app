from aws_utils import create_presigned_post


def lambda_handler(event, context):
    response = create_presigned_post(object_name=event["file_name"])
    return {"statusCode": 200, "body": response}
