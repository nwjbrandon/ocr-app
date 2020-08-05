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
    },
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "apigateway.amazonaws.com"
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

  source_code_hash = filebase64sha256("ywaste_create_presigned_post_lambda/ywaste_create_presigned_post_lambda.zip")

  runtime = "python3.7"

  environment {
    variables = {
      ACCESS_KEY = "AKIAR5L3EOIDXHL26276"
      SECRET_KEY = "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"
      REGION_NAME = "ap-southeast-1"
      BUCKET_NAME = "ywaste-receipts"
    }
  }
}

resource "aws_api_gateway_rest_api" "ywaste_lambda_apis" {
  name        = "ywaste_lambda_apis"
  description = "APIs For Ywaste Lambdas"
}

resource "aws_api_gateway_resource" "ywaste_create_presigned_post_resource" {
  path_part   = "ocr-presigned-url"
  parent_id   = aws_api_gateway_rest_api.ywaste_lambda_apis.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.ywaste_lambda_apis.id
}

resource "aws_api_gateway_method" "ywaste_create_presigned_post_method" {
  rest_api_id   = aws_api_gateway_rest_api.ywaste_lambda_apis.id
  resource_id   = aws_api_gateway_resource.ywaste_create_presigned_post_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "ywaste_create_presigned_post_integration" {
  rest_api_id             = aws_api_gateway_rest_api.ywaste_lambda_apis.id
  resource_id             = aws_api_gateway_resource.ywaste_create_presigned_post_resource.id
  http_method             = aws_api_gateway_method.ywaste_create_presigned_post_method.http_method
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = aws_lambda_function.ywaste_create_presigned_post_lambda.invoke_arn
}

resource "aws_lambda_permission" "ywaste_create_presigned_post_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ywaste_create_presigned_post_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.ywaste_lambda_apis.execution_arn}/*/*/*"
}

resource "aws_api_gateway_method_response" "ywaste_create_presigned_post_response" {
  rest_api_id = aws_api_gateway_rest_api.ywaste_lambda_apis.id
  resource_id = aws_api_gateway_resource.ywaste_create_presigned_post_resource.id
  http_method = aws_api_gateway_method.ywaste_create_presigned_post_method.http_method
  status_code = "200"
}

resource "aws_api_gateway_integration_response" "ywaste_create_presigned_post_response_integration" {
  rest_api_id = aws_api_gateway_rest_api.ywaste_lambda_apis.id
  resource_id = aws_api_gateway_resource.ywaste_create_presigned_post_resource.id
  http_method = aws_api_gateway_method.ywaste_create_presigned_post_method.http_method
  status_code = aws_api_gateway_method_response.ywaste_create_presigned_post_response.status_code
}

resource "aws_api_gateway_deployment" "ywaste_apis_deployment" {
  depends_on  = [aws_api_gateway_integration.ywaste_create_presigned_post_integration]
  rest_api_id = aws_api_gateway_rest_api.ywaste_lambda_apis.id
  stage_name  = "v1"
}
