import boto3
from botocore.exceptions import ClientError
from fastapi import FastAPI
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/instances")
def list_ec2_instances():
    instances=[]
    ec2 = boto3.client('ec2')
    regions = [r['RegionName'] for r in ec2.describe_regions()['Regions']]
    for region in regions:
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append({
                    "InstanceId": instance['InstanceId'],
                    "InstanceType": instance['InstanceType'],  
                    "Region": region,
                    "PublicIpAddress": instance.get('PublicIpAddress', 'N/A'),
                    "SecurityGroups": instance.get('SecurityGroups', []),
                })
    return instances

@app.get("/buckets")
def list_s3_buckets():
    s3 = boto3.client('s3')
    buckets = []
    for bucket in s3.list_buckets()['Buckets']:
        try:
            pab = s3.get_public_access_block(Bucket=bucket['Name'])
            public = not all(pab["PublicAccessBlockConfiguration"].values())
        except:
            public = True
        buckets.append({
            "BucketName": bucket['Name'],
            "CreationDate": bucket['CreationDate'].strftime("%Y-%m-%d %H:%M:%S"),
            "Region": s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint'],
            "Encryption": s3.get_bucket_encryption(Bucket=bucket['Name']).get('ServerSideEncryptionConfiguration', 'N/A'),
            "AccessPolicy-Public": public,
        })
    return buckets

def public_s3():
    public = [bucket for bucket in list_s3_buckets() if bucket["AccessPolicy-Public"]]
    return {
        "CIS ID": "1",
        "Description": "Ensure S3 buckets are not publicly accessible",
        "Status": "PASS" if len(public) == 0 else "FAIL",
        "Evidence": public
    }

def encryption_s3():
    unencrypted = [bucket for bucket in list_s3_buckets() if bucket["Encryption"] == 'N/A']
    return {
        "CIS ID": "2",
        "Description": "Ensure S3 buckets have encryption enabled",
        "Status": "PASS" if len(unencrypted) == 0 else "FAIL",
        "Evidence": unencrypted
    }

def IAM_no_mfa():
    iam = boto3.client('iam')
    summary = iam.get_account_summary() 
    mfa = summary['SummaryMap'].get('AccountMFAEnabled', 0)
    return {
        "CIS ID": "3",
        "Description": "Ensure IAM users have MFA enabled",
        "Status": "PASS" if mfa == 1 else "FAIL",
        "Evidence": mfa
    }

def cloudtrail_enabled():
    ct = boto3.client('cloudtrail')
    trails = ct.describe_trails()['trailList']
    return {
        "CIS ID": "4",
        "Description": "Ensure CloudTrail is enabled in all regions",
        "Status": "PASS" if len(trails) > 0 else "FAIL",
        "Evidence": trails
    }

def sec_open():
    ec2 = boto3.client('ec2')
    open_sgs = []
    regions = [r['RegionName'] for r in ec2.describe_regions()['Regions']]
    for region in regions:
        ec2 = boto3.client('ec2', region_name=region)
        sgs = ec2.describe_security_groups()['SecurityGroups']
        for sg in sgs:
            for perm in sg.get('IpPermissions', []):
                if perm.get('FromPort') in [22,3389]:
                    for ip_range in perm.get('IpRanges', []):
                        if ip_range.get('CidrIp') == '0.0.0.0/0':
                            open_sgs.append({
                                "GroupId": sg['GroupId'],
                                "Region": region,
                                "Port": perm.get('FromPort'),
                            })
    return {
        "CIS ID": "5",
        "Description": "Ensure no security groups allow unrestricted access",
        "Status": "PASS" if len(open_sgs) == 0 else "FAIL",
        "Evidence": open_sgs
    }

def store_res(results):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Visiblaze-CIS-Results')
    ts = datetime.now().isoformat()
    for result in results:
        table.put_item( 
            Item={
                'id': result['CIS ID'],
                'timestamp': ts,
                'Description': result['Description'],
                'Status': result['Status'],
                'Evidence': str(result['Evidence']),
            })

@app.get("/cis-results")
def cis_results():
    results = []
    #check 1
    results.append(public_s3())
    #check 2
    results.append(encryption_s3())
    #check 3
    results.append(IAM_no_mfa())        
    #check 4
    results.append(cloudtrail_enabled())
    #check 5
    results.append(sec_open())
    #storing these results in DynamoDB
    store_res(results)
    return results