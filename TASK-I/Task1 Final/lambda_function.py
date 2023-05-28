import boto3
import os

s3 = boto3.client("s3")

def lambda_handler(event, context):
    for record in event['Records']:
        # Get the bucket and key of the uploaded file
        bucket_name = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Check if the file is a .docx file
        if key.endswith(".docx"):
            # Generate a new key with .pdf extension
            new_key = os.path.splitext(key)[0] + ".pdf"
            
            # Copy the file to the same bucket with the new key
            s3.copy_object(Bucket=bucket_name, CopySource={'Bucket': bucket_name, 'Key': key}, Key=new_key)
            
            # Delete the old file
            s3.delete_object(Bucket=bucket_name, Key=key)

    return {
        'statusCode': 200,
        'body': 'File renamed successfully'
    }