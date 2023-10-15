import boto3
import json
import datetime
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Initialize a client
    daysDifference = 30
    fileDict = {"deleted_files":[]}
    s3_client = boto3.client('s3')

    # Specify your s3 bucket name
    s3_bucket_name = 'mahi2k'

    # Calculate the difference ex: (30 days ago)
    threshold_date = (datetime.datetime.now() - datetime.timedelta(days=daysDifference)).date()
    
    try:
        # List objects in the S3 bucket
        objects = s3_client.list_objects(Bucket=s3_bucket_name)
    
        # Delete objects that are unused and older than 30 days
        for obj in objects.get('Contents', []):
            last_modified = obj['LastModified'].date()
            if last_modified < threshold_date:
                s3_client.delete_object(Bucket=s3_bucket_name, Key=obj['Key'])
                fileDict["deleted_files"].append(s3_bucket_name|obj['Key'])
                
        return {
            "status":200,
            "body": json.dumps(fileDict)
        }
    except ClientError as e:
        return {
            "status":500,
            "body": json.dumps(e)
        }