import boto3
import os

def upload_file_to_s3(file_name, bucket_name, object_name=None):
    """Upload a file to an S3 bucket using .env config

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified, file_name is used
    :return: True if file was uploaded, else False
    """

    bucket_name = os.getenv("S3_BUCKET_NAME")
    if bucket_name is None:
        raise ValueError("S3_BUCKET_NAME not set in environment variables")

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION")
    )
    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
        print(f"Uploaded {file_name} to {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Error uploading {file_name} to {bucket_name}/{object_name}: {e}")
        return False
    return True