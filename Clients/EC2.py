from Conn.Cred_Session_Client import *
from botocore.exceptions import ClientError
import logging
import os
from requests import get
import sys
sys.argv.append('../')
import pathlib


def create_keypair(key_name):
    # Create EC2 Client
    ec2 = create_client('ec2')
    """ :type : pyboto3.ec2 """
    keys = list_keypair()
    if key_name in keys:
        print("The Given KeyPair Name already exist: "+ key_name)
    else:
        print("Creating keypair " + key_name + ".pem")
        resp = ec2.create_key_pair(
                KeyName=key_name
        )
        path = os.getcwd()
        keypair_path = os.path.abspath(os.path.join(path, os.pardir))
        with open(os.path.join("/", keypair_path, "keypair", key_name + ".pem"), 'w') as key:
            key.write(resp['KeyMaterial'])

def delete_keypair(key_name):
    # Create EC2 Client
    ec2 = create_client('ec2')
    print('deleting keypair: '+ key_name)
    resp = ec2.delete_key_pair(
        KeyName=key_name
    )
    return resp

def list_keypair():
    # Create EC2 Client
    key = []
    ec2 = create_client('ec2')
    resp = ec2.describe_key_pairs()
    for k in resp['KeyPairs']:
        key.append(k['KeyName'])
    return key


def create_instance(key_name, sg_name, inst_name):
    # Create EC2 Client
    ec2 = create_client('ec2')
    list_sg = list_sgs()
    if sg_name in list_sg:
        sg_id = list_sg[sg_name]
    else:
        sg_id = sg_ingress(sg_name)
    create_keypair(key_name)
    resp = ec2.run_instances(
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/xvdb',
                'Ebs': {
                    'VolumeSize': 10,
                    'VolumeType': 'gp2',
                    'DeleteOnTermination': True
                },
            },
        ],
        ImageId='ami-09558250a3419e7d0',  #amzon linux AMI ID: ami-0649a2ac1437cf3b7
        InstanceType='t2.micro',
        KeyName=key_name,
        MaxCount=1,
        MinCount=1,
        SecurityGroupIds=[sg_id],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': inst_name,
                    },
                ],
            },
        ],
    )
    return resp

def create_sg(sg_name):
    # Create EC2 Client
    ec2 = create_client('ec2')
    # Create security group. this will not create Ingress
    resp = ec2.create_security_group(
        Description='Ec2 SG',
        GroupName=sg_name,
        TagSpecifications=[
        {
            'ResourceType': 'security-group',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': sg_name
                },
            ]
        },
                 ]
        )
    return resp['GroupId']

def sg_ingress(sg_name):
    # Create EC2 Client
    ec2 = create_client('ec2')
    # Create security group with ingress
    sg_id = create_sg(sg_name)
    ip = my_ip()
    resp = ec2.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    'FromPort': 22,
                    'IpProtocol': 'tcp',
                    'IpRanges': [
                        {
                            'CidrIp': ip+"/32",
                            'Description': 'SSH access from my workstation',
                        },
                    ],
                    'ToPort': 22,
                },
                {
                    'FromPort': 80,
                    'IpProtocol': 'tcp',
                    'IpRanges': [
                        {
                            'CidrIp': ip+"/32",
                            'Description': 'Http access from my workstation',
                        },
                    ],
                    'ToPort': 80,
                }
            ]

    )
    return sg_id



def my_ip():
    ip = get('https://api.ipify.org').text
    return ip

def list_sgs():
    ec2 = create_client('ec2')
    resp = ec2.describe_security_groups()
    sg = resp['SecurityGroups']
    # print(sg['GroupName'])

    l_sg = {}
    for i in sg:
        key = i['GroupName']
        value = i['GroupId']
        l_sg[key] = value
    return l_sg


def get_instance_public_IP(instance_id):
    # Create EC2 Client
    ec2 = create_client('ec2')

    #Describe Instances to fet Public IP address of created instance
    resp = ec2.describe_instances(
        InstanceIds=[instance_id]
    )
    P_IP = resp['Reservations']

    for ips in P_IP:
        ip = ips['Instances']
        for i in ip:
            return '{}'.format(i['PrivateIpAddress'])


def list_instances_id():
    # Create EC2 Client
    ec2 = create_client('ec2')
    # Fetch the instance ID with its tag name in the dictionary format
    resp = ec2.describe_instances()
    ins = {}
    for reservation in resp['Reservations']:
        ins_id = reservation['Instances']
        #print(ins_id)
        for ids in ins_id:
            ID = ids['InstanceId']
            #print(ids)
            try:
                for tags in ids['Tags']:
                    val = list(tags.values())
                    if 'Name' in val:
                        ins[ID] = val[1]
            except:
                print("instance does not have Tags in it {}".format(ID))
    return ins

def terminate_instance(instance_id):
    # Create EC2 Client
    ec2 = create_client('ec2')
    print("Terminating Instance: " + instance_id)
    resp = ec2.terminate_instances(
                InstanceIds=[instance_id]
    )
    return True



def instance_status(instance_id):
    # Create EC2 Client
    ec2 = create_client('ec2')
    # Fetch the instance ID with its tag name in the dictionary format
    resp = ec2.describe_instances(
        InstanceIds=[instance_id]
    )
    for reservation in resp['Reservations']:
        state = reservation['Instances']
        for i in state:
            status = i['State']['Name']
            return status

'''
for i in range(4):
    if i == 0:
        pass
    else:
        inst = create_instance('tomy', 'tomysg', 'Boto3-ubuntu-instance')
        print(inst)
'''

ids = list_instances_id()
#print(ids)

Instances = {}
try:
    os.remove('instance_list.txt')
except:
    pass
finally:
    pathlib.Path('instance_list.txt').touch()
for i in ids:
    #print(i)
    st = instance_status(i)
    #print(st)
    if st == 'running':
        with open('instance_list.txt', 'a') as f:
            data = ids[i]+10*" "+get_instance_public_IP(i)
            f.write(data+"\n")














