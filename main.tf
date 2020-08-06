provider "aws" {
  region  = "ap-southeast-1"
}

module "ywaste_ocr_deployables" {
  source = "./deployables"
}
