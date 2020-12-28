import argparse
import glob
import sys
sys.path.append('../')
#print(sys.path)
from Clients.s3 import *



#S3 Operation:

S3_Operations = (
                "1. create_bucket",
                "2. delete_bucket",
                "3. list_bucket",
                "4. upload_objects #files",
                "5. download_objects # files",
                "6. list_objects"
                )


parser = argparse.ArgumentParser(description=S3_Operations)
parser.add_argument('-o', '--operation', choices=['list_bucket', 'create_bucket', 'delete_bucket', 'upload_objects', 'download_objects', 'list_objects'], help="choose the operation you want to perform")
parser.add_argument('-b', '--bucket_name', help='Provide Bucket Name')
parser.add_argument('-f', '--file_name', help='Provide files name to upload or download')
parser.add_argument('-r', '--region_name', help='Provide region name you want perform the operation')
args = parser.parse_args()
operation = args.operation
bucket_name = args.bucket_name
file_name = args.file_name
region_name = args.region_name


def main():
    #print(operation)
    #print(bucket_name)
    #print(file_name)
    #print(region_name)
    if operation == "list_bucket":
        out = list_buckets()
        print("listing bucket...\n" + str("\n".join(out)))
    elif operation == "create_bucket":
        out = create_bucket(bucket_name, region_name)
        print(out)
    elif operation == "delete_bucket":
        out = delete_bucket(bucket_name)
        print(out)
    elif operation == "upload_objects":
        if "*" in file_name:
            file_path = file_name
            files = glob.glob(file_path)
            for fl in files:
                out = upload_objects(fl, bucket_name)
                print(out)
        else:
            out = upload_objects(file_name, bucket_name)
            print(out)
    elif operation == "download_objects":
        out = download_objects(file_name, bucket_name)
        print(out)
    elif operation == "list_objects":
        out = list_objects(bucket_name)
        print(out)

if __name__ == '__main__':
    main()



