# requirement.txt boto3==1.34.100
from os import getenv

import boto3

ACCESS_KEY = getenv('ACCESS_KEY')
SECRET_KEY = getenv('SECRET_KEY')

s3BotoClient = boto3.client('s3',
                            aws_access_key_id=ACCESS_KEY,
                            aws_secret_access_key=SECRET_KEY
                            )


def create_bucket(bucket_name: str, aws_region_name: str):
    s3BotoClient.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
        'LocationConstraint': aws_region_name})
    # e.g:  s3BotoClient.create_bucket(Bucket='testzeebucket', CreateBucketConfiguration={'LocationConstraint': 'us-west-1'})  # need to provide location 'us-west-1' coz it is the default loction set


# ==============================================================

def list_all_bucket():
    buckets = s3BotoClient.list_buckets()

    # Print the names of all buckets.
    for bucket in buckets['Buckets']:
        print(bucket['Name'])


# ===============================================================

'''
upload file to s3 bucket
'''
def upload_file_s3(local_file_name: str, bucket_name: str, file_name_at_s3: str):
    with open(local_file_name, 'rb') as f:  # open(<file name>, 'rb')
        # Upload the file to S3
        s3BotoClient.upload_fileobj(f, bucket_name,
                                    file_name_at_s3)  # upload_fileobj(<file pointer>, <bucket name>, <file_name_at_s3>)


# ===============================================================

'''
Get the file from the bucket
'''
def get_file_from_s3(bucket_name: str, file_name_at_s3: str):
    response = s3BotoClient.get_object(Bucket=bucket_name, Key=file_name_at_s3)

    # e.g: response = s3BotoClient.get_object(Bucket='testzeebucket', Key='file_name_at_s3')
    # Read the file contents
    file_contents = response['Body'].read().decode('utf-8')
    # Print the file contents
    print(file_contents)
    return file_contents


# ================================================================

def delete_file_s3(bucket_name: str, file_name_at_s3: str):
    response = s3BotoClient.delete_object(Bucket=bucket_name, Key=file_name_at_s3)
    # e.g response = s3BotoClient.delete_object(Bucket='testzeebucket', Key='file_name_at_s3')
    print(response)
    return response


# ================================================================

if __name__ == '__main__':
    bucket_name = 'testzeebucket'
    aws_region_name = 'us-west-1'
    local_file_name = 'README.md'
    file_name_at_s3 = 'file_name_at_s3'

    create_bucket(bucket_name=bucket_name, aws_region_name=aws_region_name)
    list_all_bucket()
    upload_file_s3(local_file_name=local_file_name, bucket_name=bucket_name, file_name_at_s3=file_name_at_s3)
    downloaded_file = get_file_from_s3(bucket_name=bucket_name, file_name_at_s3=file_name_at_s3)
    delete_file_s3(bucket_name=bucket_name, file_name_at_s3=file_name_at_s3)
