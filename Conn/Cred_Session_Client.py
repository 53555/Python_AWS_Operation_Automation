import csv
from os import path
import boto3
import sys

def getting_credentials():
    file = 'new_user_credentials.csv'
    if not path.exists(file):
        sys.exit(1)
    else:
        #print("File Exist "+ file)
        Open_File = open(file, 'r')
        content = csv.reader(Open_File)
        access_key = []
        secret_key = []
        for cont in content:
              access_key.append(str(cont[2]))
              secret_key.append(str(cont[3]))
        return access_key, secret_key
        Open_File.close()


def creating_session():
    try:
        session = boto3.session.Session()
    except:
        pass
    else:
        #Getting Credential
        cred = getting_credentials()
        cred = list(cred)
        #print(cred)
        access_key_id = cred[0][1]
        secret_key = cred[1][1]
        region_name = 'us-east-2'

        #print(access_key_id, secret_key)

        #Create session object
        session = boto3.session.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_key,
            region_name=region_name
        )

    return session

def create_client(client):
    #Create Client Object
    session = creating_session()
    client_resp = session.client(client)
    """ :type : pyboto3.s3 """
    return client_resp
"""
def create_resource(client):
    #create resource object

"""







