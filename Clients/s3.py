import boto3
import sys
sys.path.append('../')
from Conn.Cred_Session_Client import *
from botocore.exceptions import ClientError
import logging
from os import path
import os
from datetime import datetime
import glob


def list_buckets():
    # Creating S3 Object
    s3 = create_client('s3')
    # Listing Bucket
    lb = s3.list_buckets()
    buckets = lb['Buckets']
    bucket_list = []
    for bucket in buckets:
        bucket_list.append(bucket['Name'])
    # print('all available buckets are: ')
    # print("=================================")
    # return "\n".join(i for i in bucket_list)
    return bucket_list


def create_bucket(bucket_name, region_name):
    try:
        location = {'LocationConstraint': region_name}
        # Creating object for list-bucket
        bucket_list = list_buckets()
        # Creating S3 Object
        s3 = create_client('s3')
        if not bucket_name in bucket_list:
            print("Creating Bucket " + bucket_name + " .....")
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration=location
            )
        else:
            print("The Bucket already Exist: " + bucket_name)
            print("=========================================")
            print("\n".join(bucket_list))

    except ClientError as e:
        logging.error(e)
        with open('error.log', 'a') as log:
            log.write(str(e))
            log.write("\n")
        return False
    return True


def delete_bucket(bucket_name):
    # Creating object for list-bucket
    bucket_list = list_buckets()
    # Creating S3 Object
    s3 = create_client('s3')
    if bucket_name in bucket_list:
        print("Deleting the bucket " + bucket_name + " .........")
        s3.delete_bucket(Bucket=bucket_name)
        print(bucket_name + " bucket been deleted")
    else:
        print("The bucket is not exist " + bucket_name)
        print("Available buckets: ", len(bucket_list))
        return "\n".join(bucket_list)


def list_objects(bucket_name):
    # Creating S3 Object
    s3 = create_client('s3')
    print("Listing Objects in the bucket " + bucket_name)
    lbo = s3.list_objects_v2(
        Bucket=bucket_name
    )
    obj_list = []
    lbo = lbo["Contents"]
    for obj in lbo:
        obj_list.append(obj['Key'])
    return "\n".join(obj_list)


def upload_objects(file_name, bucket_name):
    # Creating S3 Object
    s3 = create_client('s3')
    with open(file_name, 'rb') as data:
        print("uploading file " + file_name + " .....")
        obj = s3.upload_fileobj(
            Fileobj=data,
            Bucket=bucket_name,
            Key=file_name
        )
    return True


def download_objects(file_name, bucket_name):
    # Creating S3 Object
    s3 = create_client('s3')
    now = datetime.now()
    now = now.strftime("%Y%m%d%H%M%S")
    path = os.getcwd()
    tmp_path = os.path.abspath(os.path.join(path, os.pardir))
    #tmp_path = "/\\tmp"
    if path.exists(path.join("/", tmp_path, "tmp", file_name)):
        os.renames(path.join("/", tmp_path,"tmp", file_name), path.join("/", tmp_path, "tmp", file_name) +"_"+now)

    with open(path.join("/",tmp_path, "tmp", file_name), 'wb') as data:
        print("Downloading file "+ file_name +" ....")
        d_obj = s3.download_fileobj(
            Fileobj=data,
            Bucket=bucket_name,
            Key=file_name
        )
    return True


# upload = upload_objects('test.log', 'bhanuprakashemmadibuckettoday')
# print(upload)


# lo = list_objects('bhanuprakashemmadibuckettoday')
# print(lo)
#dw = download_objects('test.log', 'bhanuprakashemmadibuckettoday')
#print(dw)

# print("\n".join(i for i in lbucket))
'''
file_path = "C:\\Projects\\Python_AWS_Operation_Automation\\tmp\\*"
files = glob.glob(file_path)
for fl in files:
    #print("Uploading file: " + fl)
    upload_objects(fl, 'bhanuprakashemmadibuckettoday')

lbucket = list_objects('bhanuprakashemmadibuckettoday')
print(lbucket)
'''