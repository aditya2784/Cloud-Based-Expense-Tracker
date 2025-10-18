# Cloud-Based Expense Tracker

This repository contains a serverless expense tracker application built on AWS using:
- AWS Lambda (Python)
- Amazon API Gateway
- Amazon DynamoDB
- Amazon S3 (for frontend)

## Structure
See `template.yaml` for SAM deployment. Frontend is in `/frontend/index.html`.

## Quick deploy (SAM)
1. Install AWS SAM CLI
2. Configure AWS CLI (`aws configure`)
3. Build: `sam build`
4. Deploy: `sam deploy --guided`
5. After deploy, update `frontend/index.html` with the API URL

# Cloud-Based-Expense-Tracker
