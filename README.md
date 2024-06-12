# Matchday App News Feed

This repository is the source code of the AWS Lambda for the news feature in the Matchday app.

## Basic

This repository was created with [devbox](https://www.jetify.com/devbox/docs/). Go to their document for more information.

## Deploy

1. Remove `lambda_function.zip` if it already exists
2. Edit the Lambda function in `lambda_function/lambda_function.py`
3. `cd lamda_function &&  zip -r ../lambda_function.zip .`
4. Go to the [AWS console](https://ap-northeast-1.console.aws.amazon.com/lambda/home?region=ap-northeast-1#/functions/scrapingGoalcom?tab=code) and upload the zip file from the upload button on the upper-right of the code editor.


## Notes

* We have bunch of Lambda functions for Matchday app but we only have this approach for this because it uses BeautifulSoup package to croll the external website.
* Zip file is large enough so we cannot see/edit the code in AWS console.
* There must be a better approach to managing AWS Lambda in code. Please migrate to that in the future.