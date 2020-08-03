resource "aws_iam_role" "ywaste_lambda_iam" {
  name = "ywaste_lambda_iam"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "ywaste_create_presigned_post_lambda" {
  filename      = "ywaste_create_presigned_post_lambda/ywaste_create_presigned_post_lambda.zip"
  function_name = "ywaste_create_presigned_post_lambda"
  role          = aws_iam_role.ywaste_lambda_iam.arn
  handler       = "lambda_function.lambda_handler"

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  source_code_hash = filebase64sha256("ywaste_create_presigned_post_lambda/ywaste_create_presigned_post_lambda.zip")

  runtime = "python3.7"

  environment {
    variables = {
      ACCESS_KEY = "XXX"
      SECRET_KEY = "XXX"
      REGION_NAME = "XXX"
      BUCKET_NAME = "XXX"
    }
  }
}