## OCR App

### Run
- Install dependencies
```
sudo apt install python3.7 python3.7-dev python3.7-pip
python3.7 -m pip install virtualenv 
python3.7 -m virtualenv env
source env/bin/activate
pip install -r requirements.txt
```
- Go to the directory ywaste_create_presigned_post_lambda or ywaste_textract_ocr to run the file

### Linting
- Fix linting
```
./fix_lint.sh
```

### Deployment
- Install terraform
- Install aws cli
- Zip the lambda functions
```
./ywaste_create_presigned_post_lambda.sh
./ywaste_textract_ocr.sh
```
- Get the deployment files from Devops
- Apply terraform changes
```
terraform apply
```

### Best Practices
- Supports English only
- Needs high quality image of 150DPI
- Supports only PDF, JPEG, PNG
- Visually separated text and images
- Text is upright
- Cell with inconsistency column spans

### Resources
- https://stackoverflow.com/questions/30670957/creating-a-lambda-function-in-aws-from-zip-file
- https://docs.aws.amazon.com/textract/latest/dg/textract-best-practices.html
- https://ap-southeast-1.console.aws.amazon.com/textract/home?p=txt&cp=bn&ad=c&region=ap-southeast-1#/demo