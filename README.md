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
- Go to the directory src to run/edit the file

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
./deploy.sh
```
- Get the deployment files from Devops
- Apply terraform changes
```
terraform apply
```
- Ensure the files and folders .terraform/, terraform.tfstate, terraform.tfstate.backup are kept safely
- If deployment scripts fail, try to run block by block.

### Examples
- Refer to the examples code on debugging and usage.
- Ensure your image is base64 encoded when calling the api.
- Example code are executed on the repository root folder

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
- https://itnext.io/create-a-highly-scalable-image-processing-service-on-aws-lambda-and-api-gateway-in-10-minutes-7cbb2893a479
- https://www.base64-image.de/