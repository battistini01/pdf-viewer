# PDF viewer

A simple PDF viewer that returns a stored PDF in a S3 bucket, deployed as AWS Gateway API with Lambda proxy integration

PDF id must exist on database, otherwise 404 will be returned. The file name, however, is ignored.

API Gateway endpoint [example](https://pdf.livestory.io/viewer/6834895dc979d45ef5bd047d/Dummy%20PDF%20file.pdf)

# How to deploy to AWS Lambda

Build a zip package and upload to AWS

## Build zip archive
```
mkdir package
pip3 install -r requirements.txt -t package/
cp lambda_function.py package/
cd package
zip -r ../lambda_package.zip .
cd ..
```
## Update lamdba
```
aws lambda update-function-code --function-name pdf-viewer --zip-file fileb://lambda_package.zip
```
