# Cloud Posture Scanner 

Lightweight cloud posture tool that connects to an AWS account and returns the number of EC2 instances, S3 buckets and CIS Results!

## Discover Resources:
1) List all EC2 instances with: instance ID, type, region, public IP, and
associated security groups.
2) List all S3 buckets with: bucket name, region, encryption status, and
access policy (public/private).

## Run CIS AWS Benchmark Checks:
1) No S3 buckets publicly accessible.
2) All S3 buckets encrypted.
3) IAM root account has MFA enabled.
4) CloudTrail is enabled.
5) Security groups are not open to 0.0.0.0/0 for SSH or RDP.

## Store results in DynamoDB

## Expose REST APIs:
1) /instances
2) /buckets
3) /cis-results

## Frontend Dashboard:
1) Display EC2 and S3 data in tables.
2) Show CIS check results (pass/fail with evidence).

## Tech Stack:

- Backend: FastAPI, boto3
- Frontend: React
- AWS: EC2, S3, IAM, CloudTrail, DynamoDB

## How to Run: 
1) Configure AWS credentials using AWS CLI
2) Start backend:
   uvicorn main:app --reload
3) Start frontend:
   npm run dev