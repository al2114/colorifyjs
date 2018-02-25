Create a serverless project
serverless (look at get started)

create a virtualenv (pip install, it installs to virtualenv)

npm install --save serverless-python-requirements (wraps the python dependencies for deployment package)

configure serverless.yml

serverless deploy (zip up the deployment package) -> S3, sets up the lambda to load the deployment package

Create AWS Api Gateway to deploy lambda as public api

Call with ajax



microservice scrapes google image search and uses pictaculous API 
