#!/bin/bash

BUCKET_NAME="xxxxx"
STACK_NAME="render-reviver-stack"
FUNCTION_NAME="render-reviver"
ZIP_FILE="RenderReviver.zip"
TEMPLATE_FILE="template.yaml"

# Generate requirements.txt from Pipfile.lock
pipenv lock --requirements > requirements.txt

# Install dependencies into the package directory
pipenv run pip install -r requirements.txt --target ./package

cp app.py request_manager.py ./package

# Zip package directory containing function and dependencies
cd package
zip -r ../$ZIP_FILE .
cd ..

# Upload the zip file to S3
aws s3 cp $ZIP_FILE s3://$BUCKET_NAME

# Try to update the CloudFormation stack
aws cloudformation update-stack --stack-name $STACK_NAME --template-body file://$TEMPLATE_FILE --capabilities CAPABILITY_IAM

# Capture the exit status of the CloudFormation update command
CFN_UPDATE_EXIT_STATUS=$?

# If the CloudFormation update failed (non-zero exit status), then try updating the function code directly
if [ $CFN_UPDATE_EXIT_STATUS -ne 0 ]; then
    echo "CloudFormation stack update failed, trying to update the Lambda function code directly..."
    aws lambda update-function-code --function-name $FUNCTION_NAME --s3-bucket $BUCKET_NAME --s3-key $ZIP_FILE
fi
